from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('',views.settings_home,name='settings_home'),
    path('room/',views.settings_room,name='settings_room'),
    path('about_mi_board/',views.about_mi_board,name='about_mi_board'),
    path('change_room_name/<room_id>',views.change_room_name,name='change_room_name'),
]
