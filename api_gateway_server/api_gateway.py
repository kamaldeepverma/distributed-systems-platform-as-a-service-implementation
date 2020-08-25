from flask import Flask, request, Response,jsonify
import os
import requests,os

app = Flask(__name__)
app.debug = True

port_pool=9000
conf_dict={}
port_dict={}
@app.route("/test")
def checkServer():
	return "up and running"

@app.route("/data", methods = ["POST"])
def get_data():
	print(request)
	body_response={}
	token = request.get_json(force=True)["token"]
	record = request.get_json(force=True)["record"]
	print(token,' ',record)
	print(conf_dict[token])

	for i in range(5):
		record=record+',NC'

	pipeline=conf_dict[token]
	plist=pipeline.split('-')
	port_list=port_dict[token]
	# create containers


	# # # data to be sent to api
	c=plist[0]
	p=port_list[0]
	ip='172.18.16.118' 
	data = {}
	data['token']=token
	data['pipeline']= pipeline
	data['ip']=ip
	data['record'] = record
	data['port_list'] = port_list
	API_ENDPOINT='http://'+ip+':'+str(p)+'/data/'+c
	print(data)
	print(API_ENDPOINT)
	r = requests.post(API_ENDPOINT, json=data)


	body_response["status"] = 'success'
	return jsonify(body_response)

@app.route("/configuration", methods = ["POST"])
def get_configuration():
	global port_pool
	body_response={}
	user_id = request.get_json(force=True)["user_id"]
	service_pipeline_conf = request.get_json(force=True)["service_pipeline_conf"]
	print(user_id,service_pipeline_conf)
	conf_dict[user_id]=service_pipeline_conf
	
	port_list=[]
	plist = service_pipeline_conf.split('-')
	token = user_id
	for c in plist:
		if c == '1':
			port_pool=port_pool+1
			port_list.append(port_pool)
			cmd = 'docker container run --publish '+str(port_pool)+':9001 --detach --name '+token+'c1 ms1image:1'
		elif c == '2':
			port_pool=port_pool+1
			port_list.append(port_pool)
			cmd = 'docker container run --publish '+str(port_pool)+':9002 --detach --name '+token+'c2 ms2image:1'
		elif c == '3':
			port_pool=port_pool+1
			port_list.append(port_pool)
			cmd = 'docker container run --publish '+str(port_pool)+':9003 --detach --name '+token+'c3 ms3image:1'
		os.system(cmd)

	print(port_list)
	port_dict[user_id]=port_list
	print(port_dict)
	body_response["status"] = 'success'
	body_response["token"] = user_id
	return jsonify(body_response)

@app.route("/stopstream/<token>", methods = ["POST"])
def stop_stream(token):
	body_response={}
	for c in range(1,4):
		container_name=token+'c'+str(c)
		cmd = 'docker stop '+container_name
		os.system(cmd)
		cmd = 'docker rm '+container_name
		os.system(cmd)
	
	body_response["status"] = 'success'
	return jsonify(body_response)

if(__name__ == "__main__"):
	app.run(host='0.0.0.0',port = "5000")