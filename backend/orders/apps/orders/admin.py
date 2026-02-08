from django.contrib import admin

from apps.orders.models.order import Order
from apps.orders.models.order_detail import OrderDetail


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Campos que se verán como columnas en la tabla principal
    list_display = ('id', 'user_id', 'status', 'total_amount',)
    
    # Filtros laterales para buscar rápido por estado
    list_filter = ('status', 'state',)
    
    # Buscador por ID de usuario o de orden
    search_fields = ('id', 'user_id',)

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_id', 'quantity', 'unit_price',)