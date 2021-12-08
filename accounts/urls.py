from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login,name='login'),
    path('register/', views.register, name='register'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('logout/',views.logout, name='logout'),
    path('profile_edit/<user_id>/',views.profile_edit, name='profile_edit'),
    path('profile/<user_id>/',views.profile,name='profile'),
]
