from rest_framework import serializers

from .models import Recipe, Product, Category, RecipesProducts


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = [
            'name',
            'category',
        ]


class RecipesProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = RecipesProducts
        fields = [
            'product',
            'product_count',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name'
        ]


class RecipeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'products'
        ]

    def get_products(self, obj):
        return RecipesProductsSerializer(obj.recipes_products, many=True).data
