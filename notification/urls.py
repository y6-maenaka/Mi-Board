from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('get_notification/',views.get_notification,name='get_notification'),
    path('checked_notification/',views.checked_notification,name='checked_notification'),
]
