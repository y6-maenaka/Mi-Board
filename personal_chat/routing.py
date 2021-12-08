from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('<friend_id>/',consumers.PersonalChatConsumer),
]
