from django.urls import path

from .views import SubscribeToUserAPIView, UnSubscribeToUserAPIView
from . import routers

urlpatterns = [
    path('subscribe/', SubscribeToUserAPIView.as_view(), name='subscribe'),
    path('unsubscribe/', UnSubscribeToUserAPIView.as_view(), name='unsubscribe'),
] + routers.urlpatterns
