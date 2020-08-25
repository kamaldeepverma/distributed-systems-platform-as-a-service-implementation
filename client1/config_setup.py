import requests,time
import configparser

# Streaming Configurations
config = configparser.ConfigParser()
config.read("config.ini")
API_ENDPOINT = config.get("StreamingConfigurations", "PaaSAddress")
API_ENDPOINT+='/configuration'
user_id = config.get("StreamingConfigurations", "UserId")
service_pipeline_conf = config.get("StreamingConfigurations", "ServicePipelineConf")

# # # data to be sent to api 
data = {}
data['user_id']=user_id
data['service_pipeline_conf']=service_pipeline_conf 

r = requests.post(API_ENDPOINT, json=data)
token=r.json()['token']


# # update existing value
config.set('StreamingConfigurations', 'Token', token)

# # save to a file
with open('config.ini', 'w') as configfile:
    config.write(configfile)
