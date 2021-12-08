from django.urls import path
from . import views

app_name = 'stoppo'

urlpatterns = [
    path('create_directory/',views.create_directory,name='create_directory'),
    path('get_directory_data/',views.get_directory_data,name='get_directory_data'),
    path('share_file/',views.share_file,name='share_file'),
    path('store_file/',views.store_file,name='store_file'),
    path('delete_file/<file_id>/',views.delete_file,name='delete_file'),
    path('change_file_name/<file_id>/',views.change_file_name,name='change_file_name'),
    path('get_file_name/<file_id>/',views.get_file_name,name='get_file_name'),
    path('file_view/<file_id>/',views.file_view,name='file_view'),
    path('<user_id>/share_box/',views.share_box,name='share_box'),
    path('<user_id>/',views.stoppo,name='stoppo'),
]
