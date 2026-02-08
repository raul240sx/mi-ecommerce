from django.contrib import admin

from apps.products.models.product import Product
from apps.products.models.category import Category
from apps.products.models.measure_unit import MeasureUnit


class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)    

admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(Category, CategoryProductAdmin)

@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    # Campos que se verán como columnas en la tabla principal
    list_display = ('id', 'name', 'price', 'stock',)