from django.db import transaction
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from apps.products.models.product import Product
from apps.products.permissions.is_internal_service import IsInternalService


class ReserveStockView(APIView):
    permission_classes = [IsInternalService]


    def validate_item_list(self, expected_items, products_info):
        missing = []
        for item in expected_items:
            if products_info.get(item) is None:
                missing.append(item)

        if missing:
            raise ValidationError({'detail':f'No se ha encontrado el/los producto(s) con id: {missing}'})



    
    def validate_and_reserve_stock(self, items, products_info):

        for item in items:
            product = products_info.get(item['product_id'])
            if product is None:
                raise ValidationError({'detail':'Producto no encontrado para reservar stock'})
            
            try:
                if int(item['quantity']) > product.stock:
                    raise ValidationError({'detail':f'No hay suficiente stock del producto id:{item['product_id']}'})
                
                product.stock -= item['quantity']
            except (ValueError, KeyError):
                raise ValidationError({'detail':f'Error en el formato de cantidad del item id: {item['product_id']}'})



    def post(self,request):

        items = request.data.get('items')

        if request.data is None:
            return Response({'detail':'No se han enviado los id de los productos'}, status=status.HTTP_400_BAD_REQUEST)
        
        ids = []
        try:
            for item in items:
                if item['product_id'] not in ids:
                    ids.append(item['product_id'])

        except ValueError:
            return Response({'detail':'Id de productos mal formateados'}, status=status.HTTP_400_BAD_REQUEST)


        with transaction.atomic():
            products = Product.objects.select_for_update().filter(id__in=ids, state=True)
            products_info = {product.id : product for product in products}
            self.validate_item_list(ids, products_info)
            self.validate_and_reserve_stock(items, products_info)
            Product.objects.bulk_update(products, ['stock'])

            response_data = {
                str(product.id):{
                    'id':product.id,
                    'name':product.name,
                    'price':str(product.price),
                    'image_url':f'{settings.DOMAIN_URL}{product.image.url}' if product.image else None,
            } for product in products}

        return Response(response_data, status=status.HTTP_200_OK)