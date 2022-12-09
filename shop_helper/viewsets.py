from rest_framework import viewsets

from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').all()
    serializer_class = RecipeSerializer
