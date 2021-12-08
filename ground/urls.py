from django.urls import path
from . import views

app_name = 'ground'

urlpatterns = [
    path('global/',views.ground_global,name='ground_global'),
    path('local/',views.ground_local,name='ground_local'),
    path('post_ground/',views.post_ground,name='post_ground'),
]
