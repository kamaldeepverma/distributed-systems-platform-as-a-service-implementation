Steps to run 
Run the following commands in sequence

Following steps To be done at master physical node 
1. Create the Docker Images for each Microservice 

$ sh images.sh

2. Start the pricing scheduler and resource monitor server 

$ cd resource_monitoring_server
$ python3 pricing_schedular.py
$ python3 monitor_server.py

Note: Server running at http://<IP of Master Node>:9999/retrieve/<user_id>

3. Start the API Gateway Server

$ cd api_gateway_server
$ python3 api_gateway.py

Note: Server running at http://<IP of Master Node>:5000/


Following steps To be done at Slave Physical Node

1. Start resource monitor client

$ cd resource_monitoring_client
$ python3 monitor_client.py


Following steps To be done at Client Machine

$ cd client1

Note: Setup Configurations in the config.ini file and run the following commands.Tokenwill be updated on its own when we run config_setup.py.

$ python3 config_setup.py
$ python3 streaming.py



