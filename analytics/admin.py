from django.contrib import admin
from .models import DailyStats


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['bot', 'date', 'messages_sent', 'messages_received', 'new_users', 'active_users']
    list_filter = ['date', 'bot']
    search_fields = ['bot__name']
    readonly_fields = ['date']

    fieldsets = (
        ('Asosiy', {
            'fields': ('bot', 'date')
        }),
        ('Xabarlar', {
            'fields': ('messages_sent', 'messages_received')
        }),
        ('Foydalanuvchilar', {
            'fields': ('new_users', 'active_users')
        }),
        ('Engagement', {
            'fields': ('avg_response_time',)
        }),
    )