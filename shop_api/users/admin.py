from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "first_name", "last_name", "registration_source", "is_active", "is_staff")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name", "is_active", "is_staff", "registration_source")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
