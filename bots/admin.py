from django.contrib import admin
from .models import Bot, AutoReplyRule, FAQ


class AutoReplyRuleInline(admin.TabularInline):
    model = AutoReplyRule
    extra = 1
    fields = ['keywords', 'reply_text', 'is_active', 'priority']


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ['question', 'answer', 'is_active', 'order']


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['name', 'username', 'owner', 'status', 'total_users', 'total_messages', 'created_at']
    list_filter = ['status', 'auto_reply_enabled', 'created_at']
    search_fields = ['name', 'username', 'owner__username']
    readonly_fields = ['bot_id', 'total_users', 'total_messages', 'created_at', 'updated_at', 'last_active']

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('owner', 'name', 'username', 'bot_id', 'description')
        }),
        ('Token va xavfsizlik', {
            'fields': ('encrypted_token', 'webhook_secret'),
            'classes': ('collapse',)
        }),
        ('Sozlamalar', {
            'fields': ('welcome_message', 'auto_reply_enabled', 'status')
        }),
        ('Statistika', {
            'fields': ('total_users', 'total_messages', 'last_active'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [AutoReplyRuleInline, FAQInline]


@admin.register(AutoReplyRule)
class AutoReplyRuleAdmin(admin.ModelAdmin):
    list_display = ['bot', 'keywords', 'is_active', 'priority', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['keywords', 'reply_text', 'bot__name']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['bot', 'question', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer', 'bot__name']