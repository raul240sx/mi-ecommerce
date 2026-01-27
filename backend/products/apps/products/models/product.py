from django.db import models

from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.products.models.category import Category
from apps.products.models.measure_unit import MeasureUnit


class Product(BaseModel):
    name = models.CharField('Nombre producto', max_length=50)
    description = models.TextField('Descripción')
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField('Cantidad', default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products', verbose_name='Categoría del producto')
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Unidad de medida del producto')
    image = models.ImageField('Imágen del producto',upload_to='products/' , blank=True, null=True)


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name