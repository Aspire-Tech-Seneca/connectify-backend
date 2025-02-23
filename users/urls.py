from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user_profile, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update/', views.update_user_profile, name='update'),
    path('delete/', views.delete_user_profile, name='delete'),
]