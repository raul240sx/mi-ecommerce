from django.contrib import admin
from apps.products.models import MeasureUnit, Category, Product


class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')    

admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(Category, CategoryProductAdmin)
admin.site.register(Product)