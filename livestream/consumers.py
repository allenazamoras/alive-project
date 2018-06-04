from channels.generic.websocket import WebsocketConsumer
from serializers import AppealSerializer


class AppealConsumer(WebsocketConsumer):

    def connect(self):
        pass

    def disconnect(self, close_code):
        pass