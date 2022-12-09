from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории продуктов')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Категория продукта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Recipe(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название рецепта')
    products = models.ManyToManyField('Product', related_name='recipes', through='RecipesProducts', verbose_name='Продукты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipesProducts(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.PROTECT, related_name='recipes_products', verbose_name='Рецепт')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='products_recipes', verbose_name='Продукт')
    product_count = models.IntegerField(verbose_name='Количество продукта')

    def __str__(self):
        return f'{self.recipe.name} - {self.product.name}'

    class Meta:
        verbose_name = 'Продукт в рецепте'
        verbose_name_plural = 'Продукты в рецептах'
