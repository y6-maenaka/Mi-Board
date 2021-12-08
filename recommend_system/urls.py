from django.urls import path
from . import views

app_name = 'recommend_system'

urlpatterns = [
    path('recommend_board_at_main_page/',views.recommend_board_at_main_page,name='recommend_board_at_main_page'),
]
