from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.about_mi_board,name='about_mi_board'),
]
