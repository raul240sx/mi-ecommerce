from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from apps.products.api.serializers.product_serializers import ProductSerializer

from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import requests
from types import SimpleNamespace
from rest_framework import status
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    authentication_classes = ()  # evitar autenticación local por defecto
    permission_classes = []  # la validación se realiza manualmente en dispatch

    def dispatch(self, request, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            resp = Response({'detail': 'Falta Authorization header'}, status=status.HTTP_401_UNAUTHORIZED)
            # garantizar que self.headers exista antes de finalizar la response
            if not hasattr(self, 'headers'):
                self.headers = {}
            return self.finalize_response(request, resp)

        verify_url = getattr(settings, 'USERS_VERIFY_URL', 'http://users-service:8000/usuario/verify_token')
        headers = {'Authorization': auth_header}

        try:
            response = requests.get(verify_url, headers=headers, timeout=3)
        except requests.RequestException as e:
            resp = Response({'detail': f'No se puede contactar al servicio de usuarios: {e}'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
            if not hasattr(self, 'headers'):
                self.headers = {}
            return self.finalize_response(request, resp)

        if response.status_code != 200:
            resp = Response({'detail': 'Token inválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)
            if not hasattr(self, 'headers'):
                self.headers = {}
            return self.finalize_response(request, resp)

        data = response.json()
        if not data.get('valid'):
            resp = Response({'detail': data.get('error', 'Token inválido')}, status=status.HTTP_401_UNAUTHORIZED)
            if not hasattr(self, 'headers'):
                self.headers = {}
            return self.finalize_response(request, resp)

        # inyectar usuario y auth en la request para que IsAuthenticated funcione
        user_info = data.get('user', {}) or {}
        # token key (si Authorization es "Token <key>")
        token_key = auth_header.split()[1] if ' ' in auth_header else auth_header
        request.user = SimpleNamespace(is_authenticated=True, **user_info)
        request.auth = token_key

        return super().dispatch(request, *args, **kwargs)
    
    
    def get_queryset(self,pk=None):
        model = self.serializer_class.Meta.model
        if pk is None:
            return model.objects.filter(state=True)
        return model.objects.filter(id=pk,state=True).first()
    
    def list(self,request,*args, **kwargs):
        serialized_list = self.get_serializer(self.get_queryset(),many=True)
        return Response(serialized_list.data, status=status.HTTP_200_OK)


    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(
            {'message':'Producto creado correctamente',
             'data':self.get_serializer(product).data},
            status=status.HTTP_201_CREATED
            )


    def destroy(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(self.get_queryset(), id=pk)
        product.state = False
        product.deleted_date = timezone.now()
        product.save()
        return Response({'message':'Producto eliminado correctamente'},status=status.HTTP_200_OK)

    def update(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        product = get_object_or_404(self.get_queryset(),id=pk)
        serializer = self.get_serializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_product = serializer.save()
        return Response(
            {'message':'Producto actualizado correctamente',
             'data':self.get_serializer(updated_product).data},
            status=status.HTTP_200_OK 
            )













