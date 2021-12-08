from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from accounts.models import PersonalChatLayerGroup
from django.db.models import Q
from accounts.models import Users
from personal_chat.models import Message
from django.utils import timezone

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = await self.group_name()


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
        await self.last_update(self.group_name)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'send_user_id': send_user_id,
                'group_name':str(self.group_name),
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
    def group_name(self):
        user_id = Users.objects.get(username=self.scope['user']).user_id
        group_name = PersonalChatLayerGroup.objects.get(Q(invited_user_id=self.scope['url_route']['kwargs']['friend_id'],owner_user_id=user_id)|Q(invited_user_id=user_id,owner_user_id=self.scope['url_route']['kwargs']['friend_id'])).group_name
        return group_name

    @database_sync_to_async
    def store_message(self,message,send_user_id,group_name):
        new_message = Message(group_name_id=group_name,message=message,send_user_id=send_user_id)
        new_message.save()

    @database_sync_to_async
    def last_update(self,group_name):
        update_group = PersonalChatLayerGroup.objects.get(group_name=group_name)
        update_group.last_update = timezone.now()
        update_group.save()
