import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat'
        self.room_group_name = 'chat_%s' % self.room_name

        # Присоединение к группе комнаты чата
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # Принимаем соединение WebSocket

    async def disconnect(self, close_code):
        # Отключение от группы комнаты чата
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Отправка сообщения в группу комнаты чата
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except json.JSONDecodeError:
            # Обработка ошибки декодирования JSON
            await self.send(text_data=json.dumps({
                'error': 'Ошибка декодирования JSON'
            }))
        except KeyError:
            # Обработка ошибки отсутствующего ключа в JSON
            await self.send(text_data=json.dumps({
                'error': 'Отсутствует ключ "message" в JSON'
            }))

    async def chat_message(self, event):
        message = event['message']

        # Отправка сообщения обратно в WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
