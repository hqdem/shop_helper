from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .models import Recipe, RecipesProducts, Product
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        recipe_name = data['name']
        recipe_owner = request.user
        recipe = Recipe.objects.create(name=recipe_name, owner=recipe_owner)

        product_names_to_count = {item['name']: item['count'] for item in data['products']}

        recipe_to_products_list = [
            RecipesProducts(recipe=recipe, product=Product.objects.get(name=name),
                            product_count=product_names_to_count[name]) for name in product_names_to_count.keys()]

        RecipesProducts.objects.bulk_create(recipe_to_products_list)

        return Response(RecipeSerializer(recipe).data)
