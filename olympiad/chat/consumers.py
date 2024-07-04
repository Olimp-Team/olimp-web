import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olympiad.settings')
django.setup()

# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.other_user = await self.get_user(self.other_username)

        # Определяем имя комнаты как комбинацию ID пользователей
        self.room_name = f'chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}'
        self.room_group_name = self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_message(self.user, self.other_user, message)

        avatar_url = self.user.image.url if self.user.image else None

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'avatar': avatar_url,
                'id': self.user.id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        avatar = event['avatar']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'avatar': avatar,
            'id': event['id']
        }))

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def save_message(self, sender, recipient, content):
        return Message.objects.create(sender=sender, recipient=recipient, content=content)
