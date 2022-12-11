from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import Recipe, RecipesProducts, Product
from .serializers import (
    RecipeSerializer,
    ProductSerializer,
    ProductCreateUpdateSerilizer,
    RecipeCreateSerializer,
    RecipeAddProductSerializer,
    RecipeRemoveProductSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = ProductCreateUpdateSerilizer(data=data)
        if serializer.is_valid():
            product, created = serializer.save()
            if created:
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        product = self.get_object()

        serializer = ProductCreateUpdateSerilizer(product, data=data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').select_related('owner').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = RecipeCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            recipe = serializer.save()
            return Response(self.get_serializer(recipe).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk):
        data = request.data
        serializer = RecipeAddProductSerializer(data=data, context={'pk': pk})
        if serializer.is_valid():
            product_recipe, created = serializer.save()
            if created:
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def remove_product(self, request, pk):
        data = request.data
        serializer = RecipeRemoveProductSerializer(data=data)
        if serializer.is_valid():
            recipe_id = pk
            product_id = serializer.validated_data['product_id']
            instance = get_object_or_404(RecipesProducts, recipe_id=recipe_id, product_id=product_id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
