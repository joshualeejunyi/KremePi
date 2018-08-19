#!/usr/bin/env python3
import boto3
import datetime
import botocore
import json
import threading
import time
import telepot
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from picamera import PiCamera
from time import sleep
from gpiozero import Button, LED, Buzzer
from rpi_lcd import LCD
from boto3.dynamodb.conditions import Key, Attr

#declare
doorbell = Button(5, pull_up=False)
btn1 = Button(13, pull_up=False)
btn2 = Button(6, pull_up=False)
buzzer = Buzzer(19)
camera = PiCamera()
lcd = LCD()
redled = LED(23)
greenled = LED(24)
s3 = boto3.resource('s3')
tele_token = '556268385:AAF_8WfnO0P1ZaiIr5uRfv8_bYEcxuU9u5E'
bot = telepot.Bot(tele_token)
chat_id = '193372328'

#connect to aws mqtt broker
try:
	host = "a33pwtpx7h9igb.iot.us-west-2.amazonaws.com"
	rootCAPath = "rootca.pem"
	certificatePath = "certificate.pem.crt"
	privateKeyPath = "private.pem.key"
	my_rpi = AWSIoTMQTTClient("doorbell")
	my_rpi.configureEndpoint(host, 8883)
	my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
	my_rpi.configureOfflinePublishQueueing(-1)
	my_rpi.configureDrainingFrequency(2)
	my_rpi.configureConnectDisconnectTimeout(10)
	my_rpi.configureMQTTOperationTimeout(5)
	my_rpi.connect()
except Exception as e:
	print('Fatal Error %s' % e)


def doorbellpress():
	print('Waiting for doorbell press...\n')
	while True:
		if doorbell.is_pressed:
			buzzer.on()
			sleep(2)
			buzzer.off()
			ts = time.time()
			file_name = 'img'+datetime.datetime.fromtimestamp(ts).strftime('%H%M%S')+'.jpg'
			full_path = '/home/pi/Desktop/temp/'+file_name
			camera.capture(full_path)

			#upload picture to s3
			bucket_name='dexjosh-doorcam'
			s3.Object(bucket_name, file_name).put(Body=open(full_path, 'rb'),ContentType='image/jpeg',ACL='public-read')
			s3link = 'https://s3-ap-southeast-1.amazonaws.com/dexjosh-doorcam/'+file_name
			#set message payload
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			payload = json.dumps ({
				"timestamp": st,
				"imglink": s3link
				})
			#publish to broker
			my_rpi.publish("doorbell/img", payload, 1)
			#send to tele
			bot.sendPhoto(chat_id, open(full_path, 'rb'))
			bot.sendMessage(chat_id, text='Someone is at your door!')
			bot.sendMessage(chat_id, text='Go to website to accept/deny.')
			sleep(5)

def waitforreply():
	def customCallback(client, userdata, message):
		payload_dict = json.loads(message.payload)
		if payload_dict['message'] == 'granted':
			print('guest allowed.')
			lcd.clear()
			lcd.text('Access granted.', 1)
			lcd.text('Come in!', 2)
			greenled.on()
			sleep(5)
			lcd.clear()
			greenled.off()
		if payload_dict['message'] == 'denied':
			print('guest denied.')
			lcd.clear()
			lcd.text('You are not', 1)
			lcd.text('welcomed.', 2)
			redled.on()
			sleep(5)
			lcd.clear()
			redled.off()

	print('Waiting for user response... \n')
	while True:
		my_rpi.subscribe("doorbell/entry", 1, customCallback)
		sleep(5)

def catchthief():
	def customCallback2(client, userdata, message):
		payload_dict = json.loads(message.payload)
		print (payload_dict)
		if payload_dict:
			buzzer.on()
			sleep(5)
			buzzer.off()
			ts = time.time()
			file_name = payload_dict['date']+payload_dict['time']+'.jpg'
			full_path = '/home/pi/Desktop/thieftemp/'+file_name
			camera.capture(full_path)
			bucket_name='dexjosh-thief'
			s3.Object(bucket_name, file_name).put(Body=open(full_path, 'rb'),ContentType='image/jpeg',ACL='public-read')
			s3link = 'https://s3-ap-southeast-1.amazonaws.com/dexjosh-thief/'+file_name
			payload = json.dumps ({
				"date": payload_dict['date'],
				"time": payload_dict['time'],
				"event": payload_dict['event'],
				"capture": s3link
				})
			my_rpi.publish("sensors/facescan", payload, 1)
			bot.sendPhoto(chat_id, open(full_path, 'rb'))
			bot.sendMessage(chat_id, text='Someone is stealing your shoes!')
			bot.sendMessage(chat_id, text='We have captured his face, call the police.')
	print('Ready for theft capture...\n')
	while True:
		my_rpi.subscribe("doorbell/theft", 1, customCallback2)
		sleep(5)

t1 = threading.Thread(target=waitforreply)
t2 = threading.Thread(target=doorbellpress)
t3 = threading.Thread(target=catchthief)
print('Starting wait for response...')
t1.start()
print('Starting wait for doorbell...')
t2.start()
print('Starting catch theif mechanism...')
t3.start()
print('Initializing passcode system...')

# Helper class to convert a DynamoDB item to JSON.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Passcode')
Passresponse = table.query(
    KeyConditionExpression=Key('passid').eq(1)
)

for i in Passresponse['Items']:
	passcode = i.get('passcode')
print('Passcode is: '+ str(passcode))
password = [int(i) for i in str(passcode)]
userpass = []

print('Please key the passcode.\n')

def buttonOne():
	print("Button 1 pressed")
	userPass(1)
	
def buttonTwo():
	print("Button 2 pressed")
	userPass(2)
	
def userPass(number):
	print("Number received: " + str(number))
	userpass.append(number)
	print(userpass)

def checkPass(userpass, password):
	if userpass == password:
		result = True
	else:
		result = False
		
	return result
	
while True:
	lcd.text('Please Enter \nPasscode!', 1)
	btn1.when_pressed = buttonOne
	btn2.when_pressed = buttonTwo
	
	if len(userpass) == len(password):
		lcd.clear()
		lcd.text('Authenticating...', 1)
		sleep(1)
		result = checkPass(userpass, password)
		
		if result is True:
			print("Passcode Correct!\n")
			lcd.text('Passcode', 1)
			lcd.text('Correct!', 2)
			buzzer.on()
			greenled.on()
			sleep(2)
			greenled.off()
			buzzer.off()
			lcd.text('Access', 1)
			lcd.text('Granted!', 2)
			sleep(5)
			lcd.clear()
			userpass = []
		else:
			print("Wrong Passcode! \n")
			lcd.text('Passcode', 1)
			lcd.text('Incorrect!', 2)
			buzzer.on()
			redled.on()
			sleep(2)
			lcd.clear()
			redled.off()
			buzzer.off()
			userpass = []
	elif len(userpass) > len(password):
		lcd.clear()
		lcd.text('Please Try Again', 1)
		sleep(1)
		userpass = []
