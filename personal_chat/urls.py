from django.urls import path
from . import views

app_name = 'personal_chat'

urlpatterns = [
    path('',views.personal_chat,name='personal_chat'),
    path('add_talker/',views.add_talker,name='add_talker'),
    path('get_message/<friend_id>/',views.get_message,name='get_message'),
    path('register_talker/<friend_id>/',views.register_talker,name='register_talker'),
]
