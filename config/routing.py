from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from personal_chat import routing as personal_chat_routing
# from room import routing as room_chat_routing
from django.urls import path
import personal_chat.routing
import room.routing
import notification.routing


#デプロイ関係
'''https://www.sassy-blog.com/entry/20210104/1609746530'''
'''https://speakerdeck.com/denzow/djangotovuedezuo-rukanbanapurikesiyon?slide=63'''
'''https://www.slideshare.net/yuta-ishiyama/web-application-server-126087000'''

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/personal_chat/',URLRouter(personal_chat.routing.websocket_urlpatterns)),
            path('ws/room_chat/',URLRouter(room.routing.websocket_urlpatterns)),
            path('ws/',URLRouter(notification.routing.websocket_urlpatterns)),
        ])
    ),
})
