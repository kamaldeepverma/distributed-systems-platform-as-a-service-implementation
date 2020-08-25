from flask import Flask, request,jsonify
from bashCommand import run_cmd
import pika
import json
import os
flag = False
def createApp():
    credentials = pika.PlainCredentials(username='test', password='test')

    app = Flask(__name__)
    global config
    @app.route("/checkServerStatus")
    def check_server_status():
        return "server is up and running"
    
    @app.route("/configSetup", methods = ["POST"])
    def config_set_up():
        user_req = request.json
        global config 
        config = request.json['config'].split("->")
        file = open("./container_1/config.json","r+")
        json.dumps(request.json)
        file.close()
        file = open("./container_2/config.json","r+")
        json.dumps(request.json)
        file.close()
        #file = open("./container_3/config.json","r+")
        # json.dumps(request.json)
        # file.close()
        os.system("cd container_1")
        os.system("echo bits2018 | sudo -S docker build -t image_1 .")
        os.system("echo bits2018 | sudo -S docker run image_1")
        os.system("cd ../container_2")
        os.system("echo bits2018 | sudo -S docker build -t image_2 .")
        os.system("echo bits2018 | sudo -S docker run image_2")
        os.system("cd ../container_3")
        os.system("echo bits2018 | sudo -S docker build -t image_3 .")
        os.system("echo bits2018 | sudo -S docker run image_3")
        return "just testing"
    
    @app.route("/sendMessage", methods = ["POST"])
    def send_data():
        msg = request.json["msg"]
        global config
        print("config list", config)
        data={}
        for container_number in config:
            if(all(x in config for x in ["2","3"]) and len(config)==2):
                connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
                channel = connection.channel()
                channel.queue_declare(queue = "ain")
                channel.basic_publish(exchange = '', routing_key = 'ain', body = msg)
                print("Sent 1")
                print("msg is",msg)
                def result(res):
                    print("result is", res)
                    data['container_2']  = str(res)
                def result3(res):
                    print("result is", res)
                    data['container_3']  = str(res)                                    
                def callback(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result(body)
                    channel.stop_consuming()
                def callback3(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result3(body)                    
                    channel.stop_consuming()                
                channel.basic_consume(queue='aout', on_message_callback=callback, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second
                   
                channel.basic_consume(queue='aout3', on_message_callback=callback3, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second               
                #channel.start_consuming()
                connection.close()
                print("connection closed")                    
            if(all(x in config for x in ["1","2"]) and len(config)==2)    :
                connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
                channel = connection.channel()
                channel.queue_declare(queue = "ain")
                channel.basic_publish(exchange = '', routing_key = 'ain', body = msg)
                print("Sent 2")
                print("msg is",msg)
                def result(res):
                    print("result is", res)
                    data['container_2']  = str(res)
                def result2(res):
                    print("result is", res)
                    data['container_1']  = str(res)
                                                   
                def callback(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result(body)
                    channel.stop_consuming()
                def callback2(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result2(body)
                    channel.stop_consuming()
                             
                channel.basic_consume(queue='aout', on_message_callback=callback, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second
                
                channel.basic_consume(queue='aout2', on_message_callback=callback2, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second                
                
                print("connection closed")
                
            if(all(x in config for x in ["1","2","3"]) and len(config)==3):
                flag = True
                connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))
                channel = connection.channel()
                channel.queue_declare(queue = "ain")
                channel.basic_publish(exchange = '', routing_key = 'ain', body = msg)
                print("Sent 3")
                print("msg is",msg)
                def result(res):
                    print("result is", res)
                    data['container_2']  = str(res)
                def result2(res):
                    print("result is", res)
                    data['container_1']  = str(res)
                def result3(res):
                    print("result is", res)
                    data['container_3']  = str(res)                                    
                def callback(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result(body)
                    channel.stop_consuming()
                def callback2(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result2(body)
                    channel.stop_consuming()
                def callback3(ch, method, properties, body):
                    print(" [x] Received %r" % body)
                    result3(body)                    
                    channel.stop_consuming()                
                
                channel.basic_consume(queue='aout', on_message_callback=callback, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second
                
                channel.basic_consume(queue='aout2', on_message_callback=callback2, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second                
                
                channel.basic_consume(queue='aout3', on_message_callback=callback3, auto_ack=True)
                while(channel._consumer_infos):
                    channel.connection.process_data_events(time_limit=1) # 3 second               
                #channel.start_consuming()
                connection.close()
                print("connection closed")
                
        return jsonify(data)
                
    return app