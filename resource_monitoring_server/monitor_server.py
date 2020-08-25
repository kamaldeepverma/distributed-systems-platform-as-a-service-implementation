from flask import Flask, request, Response,jsonify
import os,csv,json
import requests

app = Flask(__name__)
app.debug = True

@app.route("/test")
def checkServer():
	return "up and running"

@app.route("/containers/stats", methods = ["GET"])
def get_container_stats():
	
	response_body = []

	# Local node stats
	cmd = 'echo bits2018 | sudo -S docker stats --no-stream  --format "table {{.Name}},{{.Container}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}},{{.NetIO}},{{.BlockIO}}" > stats.csv'
	os.system(cmd)
	reader = csv.DictReader(open('stats.csv', 'r'))
	dict_list = []
	for line in reader:
		dict_list.append(dict(line))
	node_stats={}
	node_stats['172.18.16.118']=dict_list
	response_body.append(node_stats)

	# node_list=['172.18.16.47','172.18.16.86']
	node_list=['172.18.16.86']
	for ip in node_list:
		API_ENDPOINT = 'http://'+ ip+':7000/containers/stats'
		r = requests.get(API_ENDPOINT)
		rlist = r.json()
		node_stats={}
		node_stats[ip]=rlist
		response_body.append(node_stats)

	
	return jsonify(response_body)

@app.route("/users/pricing", methods = ["GET"])
def get_pricing_details():
	
	# token_map=json.loads(open("token_map.json","r").read())
	token_map={}
	token_map['bb']='kamaldeepverma'
	token_map['bbc']='mayurnamjoshi'
	token_map['bbd']='vikasyadav'
	token_map['relaxed_wozniak']='siddhantjain'

	usage_time=json.loads(open("usage_time.json","r").read())
	cost_users={}
	for k,v in usage_time.items():
		#cost_users[token_map[k]]=v*79
                cost_users[k]=v*79

	return jsonify(cost_users)

@app.route("/users/pricing", methods = ["DELETE"])
def remove_pricing_details():
	
	cmd = 'rm -f usage_time.json'
	os.system(cmd)
	response_body={}
	response_body['status']='success'
	return jsonify(response_body)

if(__name__ == "__main__"):
	app.run(host='0.0.0.0',port = "6000")
