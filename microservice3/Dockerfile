FROM python:alpine
COPY . /app
WORKDIR /app
ADD . /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 9003

CMD ["python3", "service3server.py"]
#RUN python3 service1server.py 
