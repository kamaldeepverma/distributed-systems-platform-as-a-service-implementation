from flask import Flask, request, Response,jsonify
import os,csv
import requests

app = Flask(__name__)
app.debug = True

@app.route("/test")
def checkServer():
	return "up and running"

@app.route("/containers/stats", methods = ["GET"])
def get_container_stats():
	
	
	cmd = 'echo bits2018 | sudo -S docker stats --no-stream  --format "table {{.Name}},{{.Container}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}},{{.NetIO}},{{.BlockIO}}" > stats.csv'
	os.system(cmd)
	reader = csv.DictReader(open('stats.csv', 'r'))
	dict_list = []
	for line in reader:
		dict_list.append(dict(line))
	
	return jsonify(dict_list)
	
if(__name__ == "__main__"):
	app.run(host='0.0.0.0',port = "7000")
