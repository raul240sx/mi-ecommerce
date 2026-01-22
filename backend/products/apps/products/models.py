from django.db import models

from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class MeasureUnit(BaseModel):
    name = models.CharField('Unidad de medida', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de medida' 


    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name



class Category(BaseModel):
    name = models.CharField('Categoría', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField('Nombre producto', max_length=50)
    description = models.TextField('Descripción')
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='Categoría del producto')
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Unidad de medida del producto')
    image = models.ImageField('Imágen del productp',upload_to='products/' , blank=True, null=True)


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    history = HistoricalRecords(user_db_constraint=False)

    def __str__(self):
        return self.name