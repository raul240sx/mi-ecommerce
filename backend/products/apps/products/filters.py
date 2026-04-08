from django_filters import rest_framework as filters

from apps.products.models.product import Product


class ProductFilter(filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'stock': ['gt', 'lt', 'exact'],
            'price': ['gte', 'lte']
        }
