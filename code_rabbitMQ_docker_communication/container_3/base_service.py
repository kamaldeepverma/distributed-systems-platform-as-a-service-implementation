import pika as pika
import threading as threading
import queue
import time
import requests
import schedule

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
		self.recvQueueID = recvQueueID
		channel.queue_declare(queue=recvQueueID)
		self.CommLock = threading.Condition()
		self.sentMessageQueue = queue.Queue()
		channel.basic_consume(queue=recvQueueID, on_message_callback=self.onMessageReceived, auto_ack=True)
		self.senderHelper = Sender_helper(sendQueueID,rabbitMQServerIP,self.CommLock,self.sentMessageQueue)
		self.senderHelper.start()
		print("Service Initalised")
		channel.start_consuming()
	def processData(self, data):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host="172.17.0.2", credentials = credentials))
		channel = connection.channel()
		#channel.queue_declare("ain1")
		if(self.recvQueueID == "ain13"):
			processedData = str(int(data))
		else:		
			processedData = str(int(data)*5)
			#channel.basic_publish(exchange = "", routing_key = "ain13", body = processedData)
		return processedData		


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
				print("Sending to ", self.queueID, messageToSend)
				self.channel.basic_publish(exchange = "", routing_key = self.queueID, body = messageToSend)
				self.commLock.notify()
				self.commLock.release()
    
schedule.every(1).seconds.do(InitialiseService,'172.17.0.2','ain3','aout3')
schedule.every(1).seconds.do(InitialiseService,'172.17.0.2','ain13','ain3')
#schedule.every(1).seconds.do(hi)
if __name__ == "__main__":
	#for testing purposes
	#a= InitialiseService('localHost','ain','aout')
	#b= InitialiseService('localhost','aout','ain')
	while True:
		schedule.run_pending()
		#time.sleep(1)