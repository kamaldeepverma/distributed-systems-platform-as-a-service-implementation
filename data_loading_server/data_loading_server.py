from flask import Flask, request, Response,jsonify
import requests,json

app = Flask(__name__)
app.debug = True


def forward_message(record):
	print(record)

@app.route("/test")
def checkServer():
	return "up and running"

@app.route("/data/store", methods = ["POST"])
def store_data():
	# print(request)
	body_response={}
	token = request.get_json(force=True)["token"]
	record = request.get_json(force=True)["record"]
	file_name=token+'_preprocessed_data.csv'
	# print(token,record)

	with open(file_name,'a') as fd:
		fd.write(record+'\n')
		

	body_response["status"] = 'success'
	return jsonify(body_response)

@app.route("/retrieve/<token>", methods = ["GET"])
def retrieve_data(token):
	file_name=token+'_preprocessed_data.csv'
	data=[]
	body_response={}
	for line in open(file_name,"r"):
		data.append(line)
	body_response['preprocessed_data']=data
	return jsonify(body_response)
	
if(__name__ == "__main__"):
	app.run(host='0.0.0.0',port = "9999")
