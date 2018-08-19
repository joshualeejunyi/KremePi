import datetime
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
import MySQLdb
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request, Response, render_template
from flask_bootstrap import Bootstrap
from gpiozero import LED
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def index():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('VisitorLogs')
	response = table.scan()
	data = []
	final = None

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		timestamp = str(str(date) + ' ' + str(time))
		comparetime = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
		if final is not None:
			result = comparetime > final
			if result is True:
				final = comparetime
				imglink = i.get('imglink')
				accepted = i.get('accepted')
		else:
			final = comparetime
			imglink = i.get('imglink')
			accepted = i.get('accepted')
		
	d.append(final)
	d.append(imglink)
	d.append(accepted)
	data.append(d)
	return render_template('index.html', data=data[0])

@app.route("/accept/")
def acceptVisitor():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('VisitorLogs')
	response = table.scan()
	data = []
	final = None

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		timestamp = str(str(date) + ' ' + str(time))
		comparetime = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
		if final is not None:
			result = comparetime > final
			if result is True:
				final = comparetime
				imglink = i.get('imglink')
				accepted = i.get('accepted')
		else:
			final = comparetime
			imglink = i.get('imglink')
			accepted = i.get('accepted')
		
	d.append(final)
	d.append(imglink)
	d.append(accepted)
	data.append(d)
	
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
	
	dbdata = {
			"date": str(date),
			"time": str(time),
			"imglink": imglink,
			"accepted": "yes"
	}
	dbsend = json.dumps(dbdata)
	my_rpi.publish("doorbell/img", str(dbsend), 1)
	
	my_rpi.publish("doorbell/entry", "granted", 1)
	
	return render_template('index.html', data=data[0])
	
@app.route("/reject/")
def rejectVisitor():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('VisitorLogs')
	response = table.scan()
	data = []
	final = None

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		timestamp = str(str(date) + ' ' + str(time))
		comparetime = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
		if final is not None:
			result = comparetime > final
			if result is True:
				final = comparetime
				imglink = i.get('imglink')
				accepted = i.get('accepted')
		else:
			final = comparetime
			imglink = i.get('imglink')
			accepted = i.get('accepted')
		
	d.append(final)
	d.append(imglink)
	d.append(accepted)
	data.append(d)
	
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
	
	dbdata = {
			"date": str(date),
			"time": str(time),
			"imglink": imglink,
			"accepted": "no"
	}
	dbsend = json.dumps(dbdata)
	my_rpi.publish("doorbell/img", str(dbsend), 1)
	my_rpi.publish("doorbell/entry", "denied", 1)
	return render_template('index.html', data=data[0])
	
@app.route("/viewLight/")
@app.route("/viewLight/realtime/")
def viewLightRT():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Lights')
	response = table.scan()
	data = []

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		lightvalue = i.get('lightvalue')
		d.append(date)
		d.append(time)
		d.append(int(float(lightvalue) * 1024))
		data.append(d)

	data_reversed = data[::-1]
	return render_template('lights.html', data=data_reversed)
	
@app.route("/viewLight/historic/")
def viewLightHistoricRouter():
	return render_template('router.html')

@app.route("/viewLight/historic/<date>")
def viewLightHistoric(date):
	date = str(date)
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Lights')
	data = []

	response = table.query(
		KeyConditionExpression=Key('date').eq(date)
	)

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		lightvalue = i.get('lightvalue')
		d.append(date)
		d.append(time)
		d.append(int(float(lightvalue) * 1024))
		data.append(d)

	data_reversed = data[::-1]
	return render_template('lights.html', data=data_reversed)
	
@app.route("/viewLogs/")
def viewUserLogs():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('Logs')
	response = table.scan()
	data = []

	for i in response['Items']:
		currentval = i.get('event')
		if currentval == 'incoming' or currentval == 'outgoing':
			d = []
			date = i.get('date')
			time = i.get('time')
			event = i.get('event')
			facescan = i.get('facescan result')
			identity = i.get('identity')
			d.append(date)
			d.append(time)
			d.append(event)
			d.append(facescan)
			d.append(identity)
			data.append(d)
			
	data_reversed = data[::-1]
	print(data_reversed)
	return render_template('userlog.html', data = data_reversed)

@app.route("/viewThief/")
def viewThief():
	dynamodb = boto3.resource('dynamodb')

	table = dynamodb.Table('Logs')

	response = table.scan()
	data = []

	for i in response['Items']:
		currentval = i.get('event')
		if currentval == 'thief!':
			d = []
			date = i.get('date')
			time = i.get('time')
			event = i.get('event')
			capture = i.get('capture')
			d.append(date)
			d.append(time)
			d.append(event)
			d.append(capture)
			data.append(d)
			
	data_reversed = data[::-1]
	print(data_reversed)
	return render_template('thief.html', data = data_reversed)	

@app.route("/viewVisitorLogs/")
def visitorLog():
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('VisitorLogs')
	response = table.scan()
	data = []

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		imglink = i.get('imglink')
		accepted = i.get('accepted')
		d.append(date)
		d.append(time)
		d.append(imglink)
		d.append(accepted)
		data.append(d)

	print(data)
	data_reversed = data[::-1]
	return render_template('visitorlog.html', data=data_reversed)

@app.route("/viewVisitorLogs/search/")
def visitorLogsSearchRouter():
	return render_template('visitorrouter.html')
	
@app.route("/viewVisitorLogs/search/<date>/")
def visitorLogSearch(date):
	date = str(date)
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('VisitorLogs')
	response = table.scan()
	data = []

	response = table.query(
		KeyConditionExpression=Key('date').eq(date)
	)

	for i in response['Items']:
		d = []
		date = i.get('date')
		time = i.get('time')
		imglink = i.get('imglink')
		accepted = i.get('accepted')
		d.append(date)
		d.append(time)
		d.append(imglink)
		d.append(accepted)
		data.append(d)

	data_reversed = data[::-1]
	return render_template('visitorlog.html', data=data_reversed)

@app.route("/changePassword/")
def changePassword():
	return render_template('changepassword.html')
	
	
@app.route("/changePassword/<passcode>/")
def changePasswordCommit(passcode):
	passcode = str(passcode)
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
	
	dbdata = {
			"passid": 1,
			"passcode": passcode
	}
	dbsend = json.dumps(dbdata)
	my_rpi.publish("doorbell/pass", str(dbsend), 1)
	
	return render_template('passwordchanged.html')

@app.route("/registerFace/")
def registerFaceForm():
	return render_template('facescan.html')

@app.route('/registerFace/<userid>/<username>')
def registerFace(userid, username):
	from faceid import face
	face(userid)
	
	try:
		db = MySQLdb.connect("localhost", "assignmentuser", "joshsmartroom", "assignment")
		curs = db.cursor()
		print("Successfully connected to database!")
	except:
		print("Error connecting to mySQL database")

	try:
		sql = "INSERT into Users(UserID, Username) VALUES ('%d', '%s')" % (int(userid), str(username))
		curs.execute(sql)
		db.commit()
		print('\nDatabase Modified')
	except MySQLdb.Error as e:
		print(e)
	
	return render_template('faceregistered.html')
	
@app.route("/changeFaceUnlockConfidence/")
def changeConfidence():
	return render_template('changeconfidence.html')
	
@app.route("/changeFaceUnlockConfidence/<value>")
def changeConfidenceDB(value):
	value = int(value)
	try:
		db = MySQLdb.connect("localhost", "assignmentuser", "joshsmartroom", "assignment")
		curs = db.cursor()
		print("Successfully connected to database!")
	except:
		print("Error connecting to mySQL database")

	try:
		sql = "UPDATE Security SET FaceScanConfidence = %d WHERE ID = 1;" % (value)
		print(sql)
		curs.execute(sql)
		db.commit()
		print('\nDatabase Modified')
	except MySQLdb.Error as e:
		print(e)
	return render_template('confidencechanged.html')

	
if __name__ == '__main__':
	try:
		http_server = WSGIServer(('0.0.0.0', 8001), app)
		app.debug = True
		http_server.serve_forever()
	except:
		print("Exception")