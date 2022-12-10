from django.contrib import admin

from .models import *


class ProductInline(admin.TabularInline):
    model = Recipe.products.through


class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline
    ]
    search_fields = ['product__name']


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'id']
    list_display = ['id', 'name', 'category']
    readonly_fields = ['id']
    list_editable = ['category']


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipesProducts)
