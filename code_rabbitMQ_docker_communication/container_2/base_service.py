import pika as pika
import threading as threading
import queue
import time
#import requests
import schedule
import json
#from app import flag
credentials = pika.PlainCredentials(username='guest', password='guest')

def InitialiseService(rabbitMQServerIP,recvQueueID,sendQueueID):
	thread = threading.Thread(target=MicroService,args=[rabbitMQServerIP,recvQueueID,sendQueueID])
	thread.daemon = True
	thread.start()
	return thread
class MicroService():
	def __init__(self,rabbitMQServerIP,recvQueueID,sendQueueID):
		print("Initialising Service")
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQServerIP, credentials = credentials))
		channel = connection.channel()
		channel.queue_declare(queue=recvQueueID)
		self.CommLock = threading.Condition()
		self.sentMessageQueue = queue.Queue()
		channel.basic_consume(queue=recvQueueID, on_message_callback=self.onMessageReceived, auto_ack=True)
		self.senderHelper = Sender_helper(sendQueueID,rabbitMQServerIP,self.CommLock,self.sentMessageQueue)
		self.senderHelper.start()
		print("Service Initalised")
		# while(channel._consumer_infos):
		# 	channel.connection.process_data_events(time_limit=1) # 3 second
		channel.start_consuming()
	
	def processData(self,data):
		data_config = {}
		with open("config.json","r") as f:
			data_config = json.load(f)
		print(data_config['config'])
		if(all(x in data_config['config'] for x in ["1","2","3"]) or 
				all(y in data_config['config'] for y in ["1","2"])):
			connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.17.0.2", credentials = credentials))
			channel = connection.channel()
			print("sending data to ain12")
			channel.queue_declare("ain12")
			processedData = str(int(data)+1)
			channel.basic_publish(exchange = "", routing_key = "ain12", body = processedData)
		if(all(x in data_config['config'] for x in ["2","3"]) and len(data_config['config'])==3):
			connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.17.0.2", credentials = credentials))
			channel = connection.channel()
			channel.queue_declare("ain13")
			processedData = str(int(data)+1)
			print("sending data to ain13", processedData)
			channel.basic_publish(exchange = "", routing_key = "ain13", body = processedData)
		return str(int(data)+1)

	def onMessageReceived(self,ch, method, properties, message):
		print("Recvd:",message)
		#Extract Data From message
		
		#x = requests.get("http://172.18.16.47:6002/checkServerStatus")
		data = message
		#y = self.processData(data)
		#y = str(x)+y
  		
		self.sendMessage(self.processData(data))

	def sendMessage(self,message):
		if(message == ""):
			print("Error: Empty Message!")
			return
		self.CommLock.acquire()
		print(message)
		self.sentMessageQueue.put(message)
		self.CommLock.notify()
		self.CommLock.release()

class Sender_helper(threading.Thread):
	def __init__(self,queueID,serverIP,commLock,messageQueue):
		threading.Thread.__init__(self)
		connection = pika.BlockingConnection(pika.ConnectionParameters(host = serverIP, credentials = credentials))
		self.channel = connection.channel()
		self.channel.queue_declare(queue = queueID)
		self.commLock = commLock
		self.queueID = queueID
		self.messageQueue = messageQueue
		print("Sender Helper initialized")

	def run(self):
		while True:
			if(self.commLock.acquire()):
				if self.messageQueue.empty():
					self.commLock.wait()
				messageToSend = self.messageQueue.get()
				print("Sending to",self.queueID,messageToSend)
				self.channel.basic_publish(exchange = "", routing_key = self.queueID, body = messageToSend)
				self.commLock.notify()
				self.commLock.release()

schedule.every(1).seconds.do(InitialiseService,'172.17.0.2','ain','aout')
#schedule.every(1).seconds.do(hi)
if __name__ == "__main__":
	#for testing purposes
	#a= InitialiseService('locxalHost','ain','aout')
	#b= InitialiseService('localhost','aout','ain')
	while True:
		schedule.run_pending()
		#time.sleep(1)