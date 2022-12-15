from rest_framework import filters

from .models import Recipe


class RecipeByUserFilter(filters.BaseFilterBackend):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').select_related('owner').all()

    def filter_queryset(self, request, queryset, view):
        user_id = request.query_params.get('user', None)
        if not user_id:
            return queryset
        return queryset.filter(owner__id=user_id)


class RecipeBySubscribersFilter(filters.BaseFilterBackend):
    queryset = Recipe.objects.prefetch_related('recipes_products', 'recipes_products__product',
                                               'recipes_products__product__category').select_related('owner').all()

    def filter_queryset(self, request, queryset, view):
        flag = request.query_params.get('subscriptions', None)
        user = request.user
        if user.is_anonymous:
            return Recipe.objects.none()
        if not flag:
            return queryset
        return queryset.filter(owner__in=user.myuser_set.all())
