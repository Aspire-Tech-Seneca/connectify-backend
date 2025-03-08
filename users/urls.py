from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('get-user-info/', views.RetrieveUserInfoView.as_view(), name='get-user-info'),
    path('update/', views.UpdateUserProfileView.as_view(), name='update'),
    path('delete/', views.DeleteUserProfileView.as_view(), name='delete'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('upload-profile-image/', views.ProfileImageUploadView.as_view(), name='upload-profile-image'),
    path('retrieve-profile-image/', views.ProfileImageRetrieveView.as_view(), name='retrieve-profile-image'),
    path('get-interest-list/', views.InterestListView.as_view(), name='get-interests-list'),
    path('update-interest/', views.UserInterestSetView.as_view(), name='update-interest'),
    path('retrieve-interest/', views.UserInterestRetrieveView.as_view(), name='retrieve-interest'),
    path('get-recommend-matchups/', views.RecommendMatchupsView.as_view(), name='get-recommend-matchups'),
]