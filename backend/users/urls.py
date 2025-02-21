from django.urls import path
from .views import create_user, get_all_users, login_user

urlpatterns = [
    path('create/', create_user, name='create_user'),
    path('all/', get_all_users, name='get_all_users'),
    path('login/', login_user, name='login_user'),
]