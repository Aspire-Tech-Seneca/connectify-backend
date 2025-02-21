from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user_profile, name='signup'),
    path('login/', views.user_login, name='login'),
]