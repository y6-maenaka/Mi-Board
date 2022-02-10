from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('',views.top_page_board,name='top_page_board'),
    path('good_board/',views.good_board,name='good_board'),
    path('store_board/',views.store_board,name='store_board'),
    path('search_board/',views.search_board,name='search_board'),
    path('post_board/',views.post_board,name='post_board'),
    path('evaluation/',views.evaluation,name='evaluation'),
    path('reply_comment/',views.reply_comment,name='reply_comment'),
    path('confirm_view_board/<board_id>/',views.confirm_view_board,name='confirm_view_board'),
    path('board_information/<board_id>/',views.board_information,name='board_information'),
    path('<board_id>/',views.board,name='board'),
]
