from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class MeasureUnit(BaseModel):
    description = models.CharField('Descripción', max_length=50, unique=True, blank=False, null=False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return self.description


class CategoryProduct(BaseModel):
    description = models.CharField('Descripción', max_length=50, unique=True, blank=False, null=False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    
    class Meta:
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

    def __str__(self):
        return self.description


class Indicator(BaseModel):
    discount_value = models.PositiveBigIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Indicador de Ofertas')
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Indicador de Oferta'
        verbose_name_plural = 'Indicadores de Ofertas'

    def __str__(self):
        return f'Oferta de la categoría {self.category_product}: {self.discount_value}%'


class Product(BaseModel):
    name = models.CharField('Nombre de Producto', max_length=150, unique=True, blank=False, null=False)
    description = models.TextField('Descripción del Producto', unique=True, blank=False, null=False)
    stock = models.PositiveIntegerField('Stock', default=0)
    image = models.ImageField('Imágen del producto', upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de Medida', null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Categoría de Producto', related_name='productos', null=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f'Producto: {self.name}'
