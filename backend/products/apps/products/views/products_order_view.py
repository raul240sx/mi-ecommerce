from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models.product import Product


class ProductsOrderView(APIView):
    

    def get(self, request):

        ids_str = request.query_params.get('ids', None)

        if ids_str is None:
            return Response({'detail':'No se han enviado los id de los productos'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            ids_list = ids_str.split(",")
            ids_list = list(map(int, ids_list))

        except ValueError:
            return Response({'detail':'Id de productos mal formateados'}, status=status.HTTP_400_BAD_REQUEST)    

        
        products = Product.objects.filter(id__in=ids_list, state=True)

        products_dict = {
            str(product.id):{
                'id':product.id,
                'price':product.price,
                'stock':product.stock
            } for product in products
            }
        
        return Response(products_dict, status=status.HTTP_200_OK)