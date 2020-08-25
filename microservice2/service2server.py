from flask import Flask, request, Response,jsonify
from datetime import datetime,date
import requests

app = Flask(__name__)
app.debug = True


def forward_message(record):
	print(record)

@app.route("/test")
def checkServer():
	return "up and running"

@app.route("/data/2", methods = ["POST"])
def get_data():
	# print(request)
	body_response={}
	token = request.get_json(force=True)["token"]
	record = request.get_json(force=True)["record"]
	pipeline = request.get_json(force=True)["pipeline"]
	ip = request.get_json(force=True)["ip"]
	port_list = request.get_json(force=True)["port_list"]
	# print(token,record,pipeline,ip)


	#Age and Number of prime days left Calculation Business Logic
	record=record.split(',')
	date_format = "%Y-%m-%d"
	today=date.today()
	today_date_format = datetime.today().strftime('%Y-%m-%d')
	prime_expiry_date=record[11]
	born=datetime.strptime(record[4], date_format)
	prime_days_left = datetime.strptime(prime_expiry_date, date_format) - datetime.strptime(today_date_format, date_format) 
	age=today.year - born.year - ((today.month, today.day) < (born.month, born.day))
	record[15]=str(prime_days_left.days)
	record[14]=str(age)
	record=','.join(record)
	# forward_message(record)


	# # # data to be sent to api    
	plist=pipeline.split('-')
	plist=plist[1:]
	port_list=port_list[1:]
	
	
	if len(plist)!=0:
		c=plist[0]
		p=port_list[0]
		ip=ip
		data = {}
		data['token']=token
		data['pipeline']= '-'.join(plist)
		data['ip']=ip
		data['record'] = record
		data['port_list'] = port_list
		API_ENDPOINT='http://'+ip+':'+str(p)+'/data/'+c
		# print(data)
		# print(API_ENDPOINT)
		r = requests.post(API_ENDPOINT, json=data)
	else:
		# print("laast service")
		API_ENDPOINT='http://'+ip+':9999/data/store'
		data={}
		data['token']=token
		data['record']=record
		r = requests.post(API_ENDPOINT, json=data)
		# print(data)

	body_response["status"] = 'success'
	return jsonify(body_response)

	
if(__name__ == "__main__"):
	app.run(host='0.0.0.0',port = "9002")
