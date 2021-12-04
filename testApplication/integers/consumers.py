import json
from random import randint
from time import sleep
from channels.generic.websocket import WebsocketConsumer


class WSConsumer(WebsocketConsumer):  # subclass from WebsocketConsumer class
    def connect(self):
        self.accept()

        for i in range(1000):
            self.send(json.dumps({'VL1': randint(1, 100),
                                  'VL2': randint(1, 10)}))
            sleep(1)
