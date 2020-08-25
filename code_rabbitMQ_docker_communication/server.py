from flask import Flask
from flask_restful import Resource, Api , reqparse, abort
import container_initialiser
import base_service
import threading as threading
#CONFIGURATION

RABBITMQIP = '172.17.0.2'

app = Flask(__name__)
api = Api(app)

activeSessions={ }
lastTokenNumber = 0
lastQueueID = 0

def generateQID():
	global lastQueueID
	id = lastQueueID +1
	lastQueueID+=1
	return str(id)

def setupOutQ(id):
	connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQIP))
	channel = connection.channel()
	channel.queue_declare(queue = id)
	return channel


# channel.basic_publish(exchange = '', routing_key = 'a', body = msg
def InitialiseSession(id,token,config):
	thread = threading.Thread(target=Session,args=[id,token,config])
	#thread.daemon = True
	thread.start()
	return thread
class Session(base_service.MicroService):
	def __init__(self,id,token,config):
		print("Initalising Session")
		self.streamStartID = generateQID()
		self.endStreamID = generateQID()		
		super().__init__(RABBITMQIP,self.endStreamID,self.streamStartID)
		self.id = id
		self.token = token
		self.config = config
		self.containers = []
		self.processedBuffer=[]
		self.initService(1,self.streamStartID,self.endStreamID)
		global activeSessions
		activeSessions[token]=self
	
	def processData(self,data):
		self.processedBuffer.append(data)
		print(data)
	def pullData(self):
		temp = self.processedBuffer
		self.processedBuffer = []
		return temp
	def initService(self,type,inQ,outQ):
		container_initialiser.Container("./microservice1","microservice1.py",str(self.token)+"_1",RABBITMQIP,inQ,outQ).start()
		

class Configuration(Resource):
	def post(self):
		configParser = reqparse.RequestParser()
		configParser.add_argument('user_id',required=True)
		configParser.add_argument('service_pipeline_conf',required=True)
		global lastTokenNumber
		configArgs = configParser.parse_args()
		token = lastTokenNumber + 1
		lastTokenNumber+=1
		InitialiseSession(configArgs['user_id'	],token,configArgs['service_pipeline_conf'])
		return {'token':token}

class Stream(Resource):
	def post(self):
		streamParser = reqparse.RequestParser()
		streamParser.add_argument('token',required=True)
		streamParser.add_argument('record',required=True)
		streamArgs = streamParser.parse_args()
		if int(streamArgs['token']) not in activeSessions:
			abort(404,message = 'Invalid Token')
		else:
			activeSessions[int(streamArgs['token'])].sendMessage(streamArgs['record'])

class Pull(Resource):
	def get(self):
		pullParser = reqparse.RequestParser()
		pullParser.add_argument('token',required=True)
		pullArgs = pullParser.parse_args()
		if pullArgs['token'] not in activeSessions:
			abort(404,message = 'Invalid Token')
		else:
			return activeSessions[int(pullArgs['token'])].pullData()

api.add_resource(Configuration, '/configuration/')
api.add_resource(Stream, '/stream/')
api.add_resource(Pull, '/pull/')

if __name__ == '__main__':
	app.run(host='localhost',port=5000,debug=True)