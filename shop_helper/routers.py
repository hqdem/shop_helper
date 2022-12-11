from rest_framework import routers

from .viewsets import RecipeViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'products', ProductViewSet, basename='product')
urlpatterns = router.urls
