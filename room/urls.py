from django.urls import path
from . import views

app_name = 'room'

urlpatterns = [
    path('',views.room_home,name='room_home'),
    path('create_room/',views.create_room,name='create_room'),
    path('get_message/<room_id>/',views.get_message,name='get_message'),
    path('edit_room/',views.edit_room,name='edit_room'),
    path('<uuid:room_id>/',views.room,name='room'),
]
