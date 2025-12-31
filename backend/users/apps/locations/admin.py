from django.contrib import admin
from .models import Region, Commune


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "zone")
    list_filter = ("zone",)
    search_fields = ("name",)


@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")
    list_filter = ("region",)
    search_fields = ("name",)
    ordering = ("name",)
