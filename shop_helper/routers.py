from rest_framework import routers

from .viewsets import RecipeViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipy')
urlpatterns = router.urls
