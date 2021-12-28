from channels.generic.websocket import AsyncWebsocketConsumer
import json
from room.models import Rooms,RoomMessage,RoomJoining
from channels.db import database_sync_to_async
import asyncio
from django.utils import timezone
from accounts.models import Users
from room.models import Rooms
from notification.models import Notification

class RoomChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['room_id']


        self.room_group_name = str(self.group_name)

        print("チャネル接続")
        print(self.room_group_name)

        await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name,
         )

        print('チャネルグループ接続完了')

        await self.accept()

        print("チャネル完全接続完了")

    async def disconnect(self,close_code):
        print("websocketエラー")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        print('websocketは正常に閉じられました')

    # Receive message from WebSocket　JSから受信
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        send_user_id = text_data_json['send_user']

        await self.store_message(message,send_user_id,self.group_name)
        await self.update_room(self.group_name)
        await self.add_notification(message)


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
    def add_notification(self,message):
        user_id = Users.objects.get(username=self.scope['user']).user_id

        display_name = Rooms.objects.get(room_id = self.scope['url_route']['kwargs']['room_id'])

        joining_room_list = RoomJoining.objects.filter(room_id = self.scope['url_route']['kwargs']['room_id']).exclude(user_id = user_id).values_list('user_id',flat=True)
        notification_list = []

        for notification in list(joining_room_list):
            add_notification =  Notification(receiver_id=notification,room_id = self.scope['url_route']['kwargs']['room_id'],detail=message,type='room_chat',display_name=f'{display_name.room_name}')
            notification_list.append(add_notification)
        Notification.objects.bulk_create(notification_list)

    @database_sync_to_async
    def store_message(self,message,send_user_id,group_name):
        new_message = RoomMessage(message=message,send_user_id=send_user_id,room_id=group_name)
        new_message.save()

    @database_sync_to_async
    def update_room(self,group_name):
        update_room = Rooms.objects.get(room_id = group_name)
        update_room.last_update = timezone.now()
        update_room.save()
