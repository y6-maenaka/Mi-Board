from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('set_room/',views.set_room,name='set_room'),
    path('search_set_room/',views.search_set_room,name='search_set_room'),
    path('get_timetable/',views.get_timetable,name='get_timetable'),
    path('add_room_timetable/<room_id>/',views.add_room_timetable,name='add_room_timetable'),
    path('remove_seted_room/',views.remove_seted_room,name='remove_seted_room'),
    path('<user_id>/',views.mypage,name='mypage'),
]
