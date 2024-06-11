import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Message, Group
from users.models import User
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user = self.scope["user"]

            # Сохранение сообщения в базу данных
            await self.save_message(user, self.room_name, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Ошибка декодирования JSON'
            }))
        except KeyError:
            await self.send(text_data=json.dumps({
                'error': 'Отсутствует ключ "message" в JSON'
            }))

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, user, room_name, message):
        group, _ = Group.objects.get_or_create(name=room_name)
        Message.objects.create(user=user, group=group, content=message)
