from django.shortcuts import get_object_or_404
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
            'owner',
            'products'
        ]

    def get_products(self, obj):
        return RecipesProductsSerializer(obj.recipes_products, many=True).data


class ProductCreateUpdateSerilizer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=255)

    def create(self, validated_data):
        category, _ = Category.objects.get_or_create(name=validated_data['category'])
        product, created = Product.objects.get_or_create(name=validated_data['name'], category=category)
        return product, created

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        category = validated_data.get('category', instance.category)
        if isinstance(category, str):
            category, _ = Category.objects.get_or_create(name=category)
        instance.name = name
        instance.category = category
        instance.save()
        return instance


class ProductToRecipeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    count = serializers.IntegerField()


class RecipeCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    products = ProductToRecipeSerializer(many=True)

    def create(self, validated_data):
        request = self.context.get('request')
        recipe_owner = request.user

        recipe = Recipe.objects.create(name=validated_data['name'], owner=recipe_owner)

        recipe_to_products_list = [
            RecipesProducts(recipe=recipe, product=get_object_or_404(Product, name=item['name']),
                            product_count=item['count']) for item in validated_data['products']]
        RecipesProducts.objects.bulk_create(recipe_to_products_list)
        return recipe


class RecipeAddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()

    def create(self, validated_data):
        recipe_id = self.context.get('pk')
        product_id = validated_data['product_id']
        count = validated_data['count']

        instance, created = RecipesProducts.objects.get_or_create(recipe_id=recipe_id, product_id=product_id,
                                                                  defaults={'product_count': count})
        if created:
            return instance, created
        instance.product_count = count
        instance.save()
        return instance, created


class RecipeRemoveProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
