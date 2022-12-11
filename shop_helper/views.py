from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import RecipesProducts


class AddProductToRecipe(APIView):
    def post(self, request):
        data = request.data
        try:
            recipe_id = data['recipe_id']
            product_id = data['product_id']
            count = data['count']

            instance, created = RecipesProducts.objects.get_or_create(recipe_id=recipe_id, product_id=product_id, defaults={'product_count': count})
            if created:
                return Response(status=status.HTTP_201_CREATED)
            instance.product_count = count
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RemoveProductToRecipe(APIView):
    def post(self, request):
        data = request.data
        try:
            recipe_id = data['recipe_id']
            product_id = data['product_id']
            instance = get_object_or_404(RecipesProducts, recipe_id=recipe_id, product_id=product_id)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
