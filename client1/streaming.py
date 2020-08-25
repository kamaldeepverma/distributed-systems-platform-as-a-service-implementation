
import requests,time 
import configparser

# Streaming Configurations
config = configparser.ConfigParser()
config.read("config.ini")
stream_file_name = config.get("StreamingConfigurations", "StreamFileName")
stream_speed = float(config.get("StreamingConfigurations", "StreamSpeed"))
API_ENDPOINT = config.get("StreamingConfigurations", "PaaSAddress")
API_ENDPOINT+='/data'
token = config.get("StreamingConfigurations", "token")
# # data to be sent to api 
data = {'token':token} 

for row in open(stream_file_name):
    data['record']=row.rstrip('\n')
    print(data)
    r = requests.post(API_ENDPOINT, json=data)
    print(r.json())
    time.sleep(stream_speed)
    config.read("config.ini")
    stream_speed = float(config.get("StreamingConfigurations", "StreamSpeed"))


