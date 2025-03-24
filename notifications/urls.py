from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateNotificationView.as_view(), name='create'),
    path('list/', views.ListNotificationsView.as_view(), name='list'),
    path('update/', views.UpdateNotificationView.as_view(), name='update'),
]