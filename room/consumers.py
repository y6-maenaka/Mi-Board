from channels.generic.websocket import AsyncWebsocketConsumer
import json
from room.models import Rooms
from channels.db import database_sync_to_async
from room.models import RoomMessage

class RoomChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['room_id']


        self.room_group_name = str(self.group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket　JSから受信
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        send_user_id = text_data_json['send_user']

        await self.store_message(message,send_user_id,self.group_name)


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'send_user_id': send_user_id,
                'group_name': str(self.group_name),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']
        send_user_id = event['send_user_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'send_user_id':send_user_id,
        }))

    @database_sync_to_async
    def store_message(self,message,send_user_id,group_name):
        new_message = RoomMessage(message=message,send_user_id=send_user_id,room_id=group_name)
        new_message.save()
