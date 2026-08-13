from .views import RegisterAPIView, LoginAPIView
from django.urls import path

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login')
]