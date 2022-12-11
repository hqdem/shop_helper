from rest_framework import serializers

from .models import Recipe, Product, Category, RecipesProducts


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
        ]


class RecipesProductsSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = RecipesProducts
        fields = [
            'product',
        ]

    def get_product(self, obj):
        product_data = ProductSerializer(obj.product).data
        product_data['count'] = obj.product_count
        return product_data


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
