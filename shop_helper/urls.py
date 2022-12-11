from django.urls import path

from .views import *
from . import routers

urlpatterns = [
    path('add_product/', AddProductToRecipe.as_view(), name='add_product'),
    path('remove_product/', RemoveProductToRecipe.as_view(), name='remove_product'),
] + routers.urlpatterns
