from django.urls import include, path
from .views import test_mongo

urlpatterns = [
    path('test-mongo/', test_mongo, name='test_mongo'),
    path('users/', include('users.urls')),
]