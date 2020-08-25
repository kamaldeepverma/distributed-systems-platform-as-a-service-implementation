Run the following command

1. python3 server_rabbit.py
	Dynamically it will initialize all the containers through container_initialiser.py

2. microservices.py ---> contains all the codes of microservices

3. base_service.py ----> file deployed on all the containers for rabbitmq connection

4. microservice1.py  ----> microservices communicating through rabbitmq to REST server

5. app.py/server.py ----> cotaining server code
