import base_service
import sys
class Microservice1(base_service.MicroService):
	def __init__(self,rabbitMQServerIP,recvQueueID,sendQueueID):
		super.__init__(rabbitMQServerIP,recvQueueID,sendQueueID)
	
	def processData(self,record):
		record=record.split(',')
		cname=record[2]+' '+record[3]
		record[13]=cname
		record=','.join(record)
		return record
	
if __name__ == "__main__":
	base_service.InitialiseService(sys.argv[1],sys.argv[2],sys.argv[3])