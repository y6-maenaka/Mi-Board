from django.urls import path
from . import views

app_name = 'discover'

urlpatterns = [
    path('friend/',views.discover_friend,name='discover_friend'),
    path('room/',views.discover_room,name='discover_room'),
    path('change_relation_friend/',views.change_relation_friend,name='change_relation_friend'),
    path('change_relation_room/',views.change_relation_room,name='change_relation_room'),
    path('search_friend/',views.search_friend,name='search_friend'),
    path('search_room/',views.search_room,name='search_room'),
]
