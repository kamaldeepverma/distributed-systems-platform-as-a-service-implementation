FROM python:alpine
COPY . /app
WORKDIR /app
ADD . /app
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "service2server.py"]
#RUN python3 service1server.py 
