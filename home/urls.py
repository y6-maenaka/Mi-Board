from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('',views.about_mi_board,name='about_mi_board'),
    path('ranking/',views.ranking,name='ranking'),
    path('terms_of_use/',views.terms_of_use,name='terms_of_use'),
    path('privacy_policy/',views.privacy_policy,name='privacy_policy'),
]
