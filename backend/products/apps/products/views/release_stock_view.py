from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.products.permissions.is_internal_service import IsInternalService
from apps.products.models.product import Product



class ReleaseStockView(APIView):
    permission_classes = [IsInternalService]



    def add_product_stock(self, items_to_return, products_info):
        try:
            for item in items_to_return:
                product = products_info[item['product_id']]

                product.stock += int(item['quantity'])

        except ValueError:
            raise ValueError(f'Error en el formato de cantidad del item id: {item['product_id']}')



    def post(self, request):
        items = request.data.get('items')

        if items is None:
            return Response({'detail':'No se han enviado la información de los Items y la cantidad a devolver'}, status=status.HTTP_400_BAD_REQUEST)
        
        ids = []
        try:
            for item in items:
                new_id = int(item['product_id'])
                if new_id not in ids:
                    ids.append(new_id)

        except ValueError:
            return Response({'detail':'Información de items mal formateada'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            products = Product.objects.select_for_update().filter(id__in=ids, state=True)
            products_info = {product.id:product for product in products}

            self.add_product_stock(items, products_info)
            Product.objects.bulk_update(products, ['stock'])

        return Response({'detail':'Stock devuelto satisfactoriamente'}, status=status.HTTP_200_OK)
