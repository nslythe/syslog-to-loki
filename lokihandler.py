import json
import requests
from logging import StreamHandler
import time

class LokiHandler(StreamHandler):
    def __init__(self, url):
        StreamHandler.__init__(self)
        self.url = url

    def emit(self, record):
        msg = self.format(record)

        payload = {}
        payload["streams"] = []
        payload["streams"].append({})
        payload["streams"][0] = {}
        
        try:
            payload["streams"][0]["stream"] = record.tags
        except:
            payload["streams"][0]["stream"] = {}

        payload["streams"][0]["stream"]["level"] = record.levelname.lower()

        payload["streams"][0]["values"] = []
        payload["streams"][0]["values"].append([time.time_ns(), msg])

        answer = requests.post(self.url,
            data=json.dumps(payload),
            headers={
            'Content-type': 'application/json'
        })        