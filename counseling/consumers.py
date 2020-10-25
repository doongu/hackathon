import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        if user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                str(user),
                self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            str(self.scope['user']),
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        _type = data['type']
        user = self.scope['user']
        if _type == 'apply':
            application = {
                'type': 'apply',
                'name': user.name,
                'company': user.company,
                'reason': data['application']['reason']
            }
            async_to_sync(self.channel_layer.group_send)(
                str(user.counseler),
                {
                    "type": "apply",
                    "application": application,
                },
            )
        elif _type == 'accept':
            pass
        elif _type == 'message':
            pass

    def apply(self, event):
        application = event['application']
        print(application)
        self.send(text_data=json.dumps({
            'application':application
        }))
