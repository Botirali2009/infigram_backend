from rest_framework import serializers
from .models import DailyStats


class DailyStatsSerializer(serializers.ModelSerializer):
    """Kunlik statistika serializer"""
    bot_name = serializers.CharField(source='bot.name', read_only=True)

    class Meta:
        model = DailyStats
        fields = [
            'id', 'bot', 'bot_name', 'date',
            'messages_sent', 'messages_received',
            'new_users', 'active_users', 'avg_response_time'
        ]
        read_only_fields = ['id']