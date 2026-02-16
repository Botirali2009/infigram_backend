from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'plan', 'total_bots', 'total_messages', 'created_at']
    list_filter = ['plan', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumotlar", {
        'fields': ('phone', 'avatar', 'plan', 'plan_expires_at', 'total_bots', 'total_messages')
        }),
    )

    readonly_fields = ['total_bots', 'total_messages', 'created_at', 'updated_at']