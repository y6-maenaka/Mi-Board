from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('home/',views.settings_home,name='settings_home'),
    path('room/',views.settings_room,name='settings_room'),
    path('send_report/',views.send_report,name='send_report'),
    path('list_report/',views.list_report,name='list_report'),
    path('list_user_info/',views.list_user_info,name='list_user_info'),
    path('points_history',views.points_history,name='points_history'),
    path('change_room_name/<room_id>',views.change_room_name,name='change_room_name'),
]
