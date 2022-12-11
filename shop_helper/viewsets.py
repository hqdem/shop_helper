from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Recipe, RecipesProducts, Product, Category
from .serializers import RecipeSerializer, ProductSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            product_name = data['name']
            category_name = data['category']
            category, _ = Category.objects.get_or_create(name=category_name)
            product, created = Product.objects.get_or_create(name=product_name, category=category)
            if created:
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            recipe_name = data['name']
            recipe_owner = request.user
            product_names_to_count = {item['name']: item['count'] for item in data['products']}

            recipe = Recipe.objects.create(name=recipe_name, owner=recipe_owner)

            recipe_to_products_list = [
                RecipesProducts(recipe=recipe, product=get_object_or_404(Product, name=name),
                                product_count=product_names_to_count[name]) for name in product_names_to_count.keys()]

            RecipesProducts.objects.bulk_create(recipe_to_products_list)

            return Response(self.get_serializer(recipe).data, status=status.HTTP_201_CREATED)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
