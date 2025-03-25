from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateView.as_view(), name='create'),
    path('list/', views.ListView.as_view(), name='list'),
]