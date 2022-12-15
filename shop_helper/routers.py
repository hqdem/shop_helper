from rest_framework import routers

from .viewsets import RecipeViewSet, ProductViewSet, ShoppingListViewSet

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'shopping-list', ShoppingListViewSet, basename='shopping_list')
urlpatterns = router.urls
