from django.urls import path
from . import views

app_name = 'friend'

urlpatterns = [
    # path('get_friend_timetable/',views.get_friend_timetable,name='get_friend_timetable'),
    path('',views.friend_home,name='friend_home'),
    path('<friend_id>/',views.friend_profile,name='friend_profile'),
]
