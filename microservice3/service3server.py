from flask import Flask, request, Response,jsonify

# sudo pip3 install CurrencyConverter

from currency_converter import CurrencyConverter
from datetime import datetime,date
from pytz import timezone

import requests

app = Flask(__name__)
app.debug = True

def forward_message(record):
	print(record)

@app.route("/test")
def checkServer():
	return "up and running"

@app.route("/data/3", methods = ["POST"])
def get_data():
	# print(request)
	body_response={}
	token = request.get_json(force=True)["token"]
	record = request.get_json(force=True)["record"]
	pipeline = request.get_json(force=True)["pipeline"]
	ip = request.get_json(force=True)["ip"]
	port_list = request.get_json(force=True)["port_list"]
	# print(token,record,pipeline,ip)


	#Currency Conversion business logic
	record=record.split(',')
	c = CurrencyConverter()
	standard_price=c.convert(record[6], record[10], 'INR')
	record[16]=str(standard_price)
		
	#Time Conversion business logic
	ts_format = "%Y-%m-%d %H:%M:%S"
	order_timestamp_str = record[8]
	order_timestamp_obj = datetime.strptime(order_timestamp_str, ts_format)
	order_timestamp_obj = timezone(record[12]).localize(order_timestamp_obj)
	order_timestamp_utc = order_timestamp_obj.astimezone(timezone('UTC'))
	record[17]=order_timestamp_utc.strftime(ts_format)
	# print(record)
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
	app.run(host='0.0.0.0',port = "9003")
