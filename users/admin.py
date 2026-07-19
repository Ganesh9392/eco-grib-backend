from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ["username", "email", "role", "building", "is_active"]
    list_filter = ["role", "is_active", "building"]
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Eco-Grid", {"fields": ("role", "building")}),
    )
