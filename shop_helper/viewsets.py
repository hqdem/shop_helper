from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

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
from .filters import RecipeByUserFilter


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return Product.objects.select_related('category').all()

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
    filter_backends = [RecipeByUserFilter]

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

    @action(detail=True, methods=['post'])
    def add_like(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if user in recipe.dislikes.all():
            recipe.dislikes.remove(user)
        recipe.likes.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def add_dislike(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if user in recipe.likes.all():
            recipe.likes.remove(user)
        recipe.dislikes.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def remove_like(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        recipe.likes.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def remove_dislike(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        recipe.dislikes.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
