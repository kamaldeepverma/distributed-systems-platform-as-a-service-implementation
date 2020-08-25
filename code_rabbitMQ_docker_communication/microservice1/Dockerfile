FROM python:alpine
COPY . /app
WORKDIR /app
ADD . /app
EXPOSE 3333:3333
RUN python3 -m pip install -r requirements.txt

RUN python3 microservice1.py 172.17.0.2 1 2