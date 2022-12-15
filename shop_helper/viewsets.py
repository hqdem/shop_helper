from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from .models import Recipe, RecipesProducts, Product, ShoppingList
from .serializers import (
    RecipeSerializer,
    ProductSerializer,
    ProductCreateUpdateSerilizer,
    RecipeCreateSerializer,
    RecipeAddProductSerializer,
    RecipeRemoveProductSerializer,
    UserSerializer,
    ShoppingListSerializer,
    ShoppingListCreateSerializer,
    ProductToShoppingListSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .filters import RecipeByUserFilter, RecipeBySubscribersFilter


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


class ShoppingListViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShoppingListSerializer

    def get_object(self):
        return get_object_or_404(ShoppingList.objects.prefetch_related('products__category').select_related('owner'),
                                 owner=self.request.user)

    @action(methods=['get'], detail=False)
    def get_list(self, request):
        return Response(ShoppingListSerializer(self.get_object()).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def create_list(self, request):
        data = request.data
        serializer = ShoppingListCreateSerializer(data=data)
        if serializer.is_valid():
            serializer_data = serializer.data
            product_ids = [product_id['product_id'] for product_id in serializer_data['products']]
            name = serializer_data['name']

            user = request.user
            products = Product.objects.filter(id__in=product_ids)

            instance, created = ShoppingList.objects.prefetch_related('products__category').select_related(
                'owner').get_or_create(owner=user)
            if created:
                instance.name = name
                instance.products.add(*products)
                instance.save()
                return Response(ShoppingListSerializer(instance).data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def add_product(self, request):
        data = request.data
        serializer = ProductToShoppingListSerializer(data=data)
        if serializer.is_valid():
            serializer_data = serializer.data
            product = get_object_or_404(Product, pk=serializer_data['product_id'])
            instance = self.get_object()
            instance.products.add(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def remove_product(self, request):
        data = request.data
        serializer = ProductToShoppingListSerializer(data=data)
        if serializer.is_valid():
            serializer_data = serializer.data
            product = get_object_or_404(Product, pk=serializer_data['product_id'])
            instance = self.get_object()
            instance.products.remove(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').select_related('owner').all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [RecipeByUserFilter, RecipeBySubscribersFilter]

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

    @action(detail=True, methods=['get'])
    def likes(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        likes = recipe.likes.all()
        return Response(UserSerializer(likes, many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def dislikes(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        dislikes = recipe.dislikes.all()
        return Response(UserSerializer(dislikes, many=True).data, status=status.HTTP_200_OK)
