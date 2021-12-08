from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from accounts.models import Users
from personal_chat.models import PersonalChatLayerGroup
from django.db.models import Q
from room.models import RoomJoining,Rooms

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.all_room_name = await self.all_group_name()

        for room in self.all_room_name:
            await self.channel_layer.group_add(
                str(room),
                self.channel_name
            )

        await self.accept()

    async def disconnect(self,close_code):
        for room in self.all_room_name:
            await self.channel_layer.group_add(
                str(room),
                self.channel_name
            )

    # Receive message from WebSocket　JSから受信
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        send_user_id = text_data_json['send_user']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'send_user_id': send_user_id,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']
        send_user_id = event['send_user_id']
        group_name = event['group_name']

        notification_detail = await self.group_data(group_name)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'send_user_id':send_user_id,
            'notification_detail':notification_detail,
        }))

    @database_sync_to_async
    def all_group_name(self):
        all_group_name = []
        user_id = user_id = Users.objects.get(username=self.scope['user']).user_id
        personal_chat_group_name = list(PersonalChatLayerGroup.objects.filter(Q(invited_user_id = user_id)|Q(owner_user_id = user_id)).values_list('group_name',flat=True))
        room_chat_group_name = list(RoomJoining.objects.filter(user_id = user_id).values_list('room_id',flat=True))
        all_group_name = personal_chat_group_name+room_chat_group_name
        return all_group_name

    @database_sync_to_async
    def group_data(self,group_name):
        try:
            user_id = Users.objects.get(username=self.scope['user']).user_id
            friend_id = PersonalChatLayerGroup.objects.get(group_name=group_name)
            if friend_id.invited_user_id == user_id:
                user_id = friend_id.owner_user_id
            else:
                user_id = friend_id.invited_user_id

            user_data = Users.objects.get(user_id = user_id)
            notification_detail = str(f'{user_data.last_name}{user_data.first_name}')
        except:
            room_data = Rooms.objects.get(room_id = group_name)
            notification_detail = str(room_data.room_name)

        return notification_detail
