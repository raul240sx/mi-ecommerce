from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fk_name = "user"  # importante porque Address tiene 2 ForeignKey a User (user y deleted_by)
    fields = ("street", "number", "apartment", "commune", "is_main", "is_active")
    readonly_fields = ("is_active", "deleted_at", "deleted_by")


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "phone")}),
        ("Estado", {"fields": ("is_active", "is_staff")}),
        ("Borrado lógico", {"fields": ("deleted_at", "deleted_by")}),
    )

    readonly_fields = ("deleted_at", "deleted_by")

    inlines = [AddressInline]


admin.site.register(User, UserAdmin)
