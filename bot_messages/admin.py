from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'message_type', 'text_preview', 'is_read', 'created_at']
    list_filter = ['sender', 'message_type', 'is_read', 'is_forwarded', 'created_at']
    search_fields = ['text', 'chat__username', 'chat__first_name']
    readonly_fields = ['telegram_message_id', 'created_at']

    fieldsets = (
        ('Chat ma\'lumotlari', {
            'fields': ('chat', 'telegram_message_id', 'sender')
        }),
        ('Xabar', {
            'fields': ('message_type', 'text', 'file_id', 'file_path', 'file_size')
        }),
        ('Reply/Forward', {
            'fields': ('reply_to', 'is_forwarded'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_deleted')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )

    def text_preview(self, obj):
        """Matn preview"""
        if obj.text:
            return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
        return f"[{obj.message_type}]"

    text_preview.short_description = 'Xabar'