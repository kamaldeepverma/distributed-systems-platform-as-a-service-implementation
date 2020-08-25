from flask import Flask
from flask_restful import Resource, Api , reqparse, abort

app = Flask(__name__)
api = Api(app)

activeSessions={ }
lastTokenNumber = 0



class Session():
	def __init__(self,id,token,config):
		self.id = id
		self.token = token
		self.config = config
		self.initialiseService(config.split('-'))
		#setup message queues

	def initialiseService(self,config):
		for serviceType in config:
            
    def initialiseContainer                 

	def postData(self,record):
		pass

	def pullData(self):
		pass

class Configuration(Resource):
	def post(self):
		configParser = reqparse.RequestParser()
		configParser.add_argument('user_id',required=True)
		configParser.add_argument('service_pipeline_conf',required=True)
		configArgs = configParser.parse_args()
		token = lastTokenNumber + 1
		lastTokenNumber+=1
		session = Session (configArgs['user_id'], token , configArgs['service_pipeline_conf'])
		activeSessions['token']=session
		return {token}

class Stream(Resource):
	def post(self):
		streamParser = reqparse.RequestParser()
		streamParser.add_argument('token',required=True)
		streamParser.add_argument('record',required=True)
		streamArgs = streamParser.parse_args()
		if streamArgs['token'] not in activeSessions:
			abort(404,message = 'Invalid Token')
		else:
			activeSessions[streamArgs['token']].postData(streamArgs['record'])

class Pull(Resource):
	def get(self):
		pullParser = reqparse.RequestParser()
		pullParser.add_argument('token',required=True)
		pullArgs = pullParser.parse_args()
		if pullArgs['token'] not in activeSessions:
			abort(404,message = 'Invalid Token')
		else:
			return activeSessions[pullArgs['token']].pullData(pullArgs['record'])

api.add_resource(Configuration, '/configuration/')
api.add_resource(Stream, '/stream/')
api.add_resource(Pull, '/pull/')

if __name__ == '__main__':
	app.run(host='localhost',port=5000,debug=True)