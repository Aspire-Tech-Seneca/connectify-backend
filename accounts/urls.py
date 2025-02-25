from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.create_user_profile, name='signup'),
    path('login/', views.user_login, name='login'),
]
