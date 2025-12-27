from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "is_active", "is_staff")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password", "is_active", "is_staff")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
