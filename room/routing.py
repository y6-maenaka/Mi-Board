from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('<room_id>/',consumers.RoomChatConsumer),
]
