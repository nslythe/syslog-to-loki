FROM ubuntu

RUN apt-get update -y && apt-get install -y python3.10 python3-pip

RUN mkdir /app
COPY *.py /app
COPY requirements.txt /app

WORKDIR /app

RUN python3.10 -m pip install -r requirements.txt

STOPSIGNAL SIGINT

ENTRYPOINT python3.10 main.py