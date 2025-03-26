from django.urls import path
from . import views
from rest_framework.authtoken import views as token_views

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
    path('delete-gallery-image/', views.GalleryImageDeleteView.as_view(), name='delete-gallery-image'),
    path('get-interest-list/', views.InterestListView.as_view(), name='get-interests-list'),
    path('update-interest/', views.UserInterestSetView.as_view(), name='update-interest'),
    path('retrieve-interest/', views.UserInterestRetrieveView.as_view(), name='retrieve-interest'),
    path('get-recommend-matchups/', views.RecommendMatchupsView.as_view(), name='get-recommend-matchups'),
    path('request-matchup/', views.RequestMatchupAPIView.as_view(), name='request-matchup'),
    path('get-matchup-status/', views.GetMatchupStatusAPIView.as_view(), name='get-matchup-status'),
    path('confirm-matchup-request/', views.ConfirmMatchupRequestAPIView.as_view(), name='confirm-matchup-request'),
    path('get-mymatchup-list/', views.GetMyMatchupListAPIView.as_view(), name='get-mymatchup-list'),
    path('deny-matchup-request/', views.DenyMatchupRequestAPIView.as_view(), name='deny-matchup-request'),
    path('block-matchup-request/', views.BlockMatchupRequestAPIView.as_view(), name='block-matchuprequest'),
    # API endpoints
    path('api/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
]