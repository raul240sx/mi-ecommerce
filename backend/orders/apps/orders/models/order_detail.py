from django.db import models

from simple_history.models import HistoricalRecords


class OrderDetail(models.Model):
    product_id = models.IntegerField('ID del producto')
    product_title = models.CharField('Nombre del producto', max_length=50, blank=True, null=True)
    quantity = models.IntegerField('Cantidad del producto')
    unit_price = models.DecimalField('Precio unitario', max_digits=8, decimal_places=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')


    class Meta:
        verbose_name = 'Detalle de Orden'
        verbose_name_plural = 'Detalles de orden'


    history = HistoricalRecords(user_db_constraint=False)


    def __str__(self):
        return f'Producto {self.product_id} - Cantidad {self.quantity}, Orden {self.order}'