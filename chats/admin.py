from django.contrib import admin
from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'bot', 'telegram_user_id', 'message_count', 'is_blocked', 'last_message_at']
    list_filter = ['is_blocked', 'is_active', 'created_at']
    search_fields = ['telegram_user_id', 'username', 'first_name', 'last_name', 'phone', 'email']
    readonly_fields = ['telegram_user_id', 'message_count', 'created_at', 'updated_at', 'last_message_at']

    fieldsets = (
        ('Telegram ma\'lumotlari', {
            'fields': ('bot', 'telegram_user_id', 'username', 'first_name', 'last_name')
        }),
        ('Aloqa ma\'lumotlari', {
            'fields': ('phone', 'email'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_blocked', 'is_active')
        }),
        ('Statistika', {
            'fields': ('message_count', 'last_message_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )