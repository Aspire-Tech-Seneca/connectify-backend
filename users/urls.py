from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('update/', views.UpdateUserProfileView.as_view(), name='update'),
    path('delete/', views.DeleteUserProfileView.as_view(), name='delete'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password')
]