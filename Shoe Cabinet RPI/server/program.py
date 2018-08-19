from gpiozero import Button, MCP3008, LED, Buzzer
from rpi_lcd import LCD
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
import json
import cv2
import numpy as np
import os 
import MySQLdb
from time import sleep
import string
import time, datetime
from picamera import PiCamera
import subprocess

adc = MCP3008(channel=0)
whitebutton = Button(13, pull_up=False)
redbutton = Button(5, pull_up=False)
lcd = LCD()
lcd.clear()
dbaction = None
timeout = None

host = "a33pwtpx7h9igb.iot.us-west-2.amazonaws.com"
rootCAPath = "../keys/rootca.pem"
certificatePath = "../keys/certificate.pem.crt"
privateKeyPath = "../keys/private.pem.key"

my_rpi = AWSIoTMQTTClient("joshpubsub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec
my_rpi.connect()

def lightcheck():
	lightvalue = adc.value
	return lightvalue

def greenLED():
	greenled = LED(23)
	greenled.on()
	sleep(1)
	greenled.off()
	greenled.close()	

def redLED():
	redled = LED(18)
	redled.on()
	sleep(1)
	redled.off()
	redled.close()

def buzzBuzz():
	buzz = Buzzer(21)
	buzz.on()
	sleep(1)
	buzz.off()
	buzz.close()
	
while True:
	lcd.text("White: Come Home", 1)
	lcd.text("Red: Leave House", 2)
	whitepress = whitebutton.is_pressed
	redpress = redbutton.is_pressed
	if whitepress is True:
		dbaction = 'incoming'
		break
	elif redpress is True:
		dbaction = 'outgoing'
		break
	else:
		lightvalue = lightcheck()
		dbdata = {
			"date": str(datetime.date.today()),
			"time": str(datetime.datetime.now().time()),
			"lightvalue": str(lightvalue)
		}
		dbsend = json.dumps(dbdata)
		my_rpi.publish("sensors/light", str(dbsend), 1)
		print(dbsend)
		print('LIGHT')
		print(lightvalue)
		if lightvalue < 0.5:
			timestamp = datetime.datetime.now()
			if timeout is not None:
				timediff = timestamp - timeout
				
				if timediff > datetime.timedelta(minutes = 3):
					logsdata = {
						"date": str(datetime.date.today()),
						"time": str(datetime.datetime.now().time()),
						"event": "thief!"
					}
					logsdbsend = json.dumps(logsdata)
					print(dbsend)
					my_rpi.publish("sensors/facescan", str(logsdbsend), 1)
					my_rpi.publish("doorbell/theft", str(logsdbsend), 1)
					timeout = timestamp
			else:
				buzzBuzz()
				logsdata = {
					"date": str(datetime.date.today()),
					"time": str(datetime.datetime.now().time()),
					"event": "thief!"
				}
				logsdbsend = json.dumps(logsdata)
				print(dbsend)
				my_rpi.publish("sensors/facescan", str(logsdbsend), 1)
				my_rpi.publish("doorbell/theft", str(logsdbsend), 1)
				timeout = timestamp
lcd.clear()
whitebutton.close()
redbutton.close()
adc.close()

subprocess.call(["sudo", "modprobe", "bcm2835-v4l2"])
lcd = LCD()
lcd.text('Initializing', 1)
lcd.text('Face Scan...', 2)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../trainer/trainer.yml')
cascadePath = "../haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

try:
	db = MySQLdb.connect("localhost", "assignmentuser", "joshsmartroom", "assignment")
	curs = db.cursor()
	print("Successfully connected to database!")
except:
	print("Error connecting to mySQL database")

sql = "SELECT Username FROM assignment.Users"
curs.execute(sql)
result = curs.fetchall()
userslist = ['None']

for x in range(0, len(result)):
	userslist.append(result[x][0])

print(userslist)
# Initialize database
sql = "SELECT FaceScanConfidence FROM assignment.Security"
curs.execute(sql)
result = curs.fetchall()
setconfidence = int(result[0][0])

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

lcd.clear()
lcd.text('Scanning...', 1)
starttime = time.time()
while True:
	confidentint = 0
	ret, img =cam.read()
	img = cv2.flip(img, -1) # Flip vertically
	
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale( 
		gray,
		scaleFactor = 1.2,
		minNeighbors = 5,
		minSize = (int(minW), int(minH)),
		)
	
	for(x,y,w,h) in faces:
		cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
		id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
		
		# Check if confidence is less them 100 ==> "0" is perfect match 
		if (confidence < 100):
			id = userslist[id]
			confidentint = round(100 - confidence)
			print(confidentint)
			confidence = "  {0}%".format(round(100 - confidence))
		else:
			id = "unknown"
			confidence = "  {0}%".format(round(100 - confidence))
        
		cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
		cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

	#cv2.imshow('camera',img) 
	if confidentint > setconfidence:
		lcd.text('Identity', 1)
		lcd.text('Confirmed!', 2)
		buzzBuzz()
		greenLED()
		lcd.clear()
		if dbaction == 'incoming':
			lcd.text('Welcome Home,',  1)
			lcd.text(str(id) + '!', 2)
		else:
			lcd.text('Goodbye,' + str(id), 1)
		
		logsdata = {
			"date": str(datetime.date.today()),
			"time": str(datetime.datetime.now().time()),
			"event": dbaction,
			"facescan result": "success",
			"identity": id
		}
		dbsend = json.dumps(logsdata)
		my_rpi.publish("sensors/facescan", str(dbsend), 1)
		sleep(5)	
		break
		
	nowtime = time.time()
	timediff = nowtime - starttime
	if timediff > 30:
		redLED()
		buzzBuzz()
		cam.release()
		cv2.destroyAllWindows()
		lcd.text('Identity', 1)
		lcd.text('Unconfirmed!', 2)
		logsdata = {
			"date": str(datetime.date.today()),
			"time": str(datetime.datetime.now().time()),
			"event": dbaction,
			"facescan result": "fail"
		}
		dbsend = json.dumps(logsdata)
		print(dbsend)
		my_rpi.publish("sensors/facescan", str(dbsend), 1)
		sleep(5)
		break

sleep(60)
lcd.clear()
import program