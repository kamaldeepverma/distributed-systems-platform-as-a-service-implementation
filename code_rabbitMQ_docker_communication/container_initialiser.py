import os
BOILERPLATE ='''FROM python:alpine
COPY . /app
WORKDIR /app
ADD . /app
EXPOSE 3333:3333
RUN python3 -m pip install -r requirements.txt
'''

class Container():
	def __init__(self,path,appName,name,rabbitIP,inQ,outQ):
		print("Initialising Container")
		self.name = name
		self.inQ = inQ
		self.outQ = outQ
		self.path = path
		dockerFile = open(path+'/Dockerfile','w+')
		dockerFile.write(BOILERPLATE)
		dockerFile.write('\nRUN python3 '+appName+" "+rabbitIP+" "+self.inQ+" "+self.outQ)
		dockerFile.close()
	def start(self):
		os.system("echo bits2018 | sudo -S docker build -t "+self.name+" "+self.path)