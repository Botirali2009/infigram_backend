from rest_framework import serializers
from .models import Bot, AutoReplyRule, FAQ


class BotSerializer(serializers.ModelSerializer):
    """Bot serializer"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Bot
        fields = [
            'id', 'owner', 'owner_username', 'name', 'username', 'bot_id',
            'description', 'welcome_message', 'auto_reply_enabled',
            'status', 'total_users', 'total_messages', 'created_at', 'last_active'
        ]
        read_only_fields = ['id', 'bot_id', 'total_users', 'total_messages', 'created_at', 'last_active']


class BotCreateSerializer(serializers.Serializer):
    """Bot qo'shish uchun"""
    name = serializers.CharField(max_length=255)
    token = serializers.CharField(write_only=True)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_token(self, value):
        """Token formatini tekshirish"""
        if not value or ':' not in value:
            raise serializers.ValidationError("Noto'g'ri bot token!")
        return value


class AutoReplyRuleSerializer(serializers.ModelSerializer):
    """Auto Reply serializer"""

    class Meta:
        model = AutoReplyRule
        fields = ['id', 'bot', 'keywords', 'reply_text', 'is_active', 'priority', 'created_at']
        read_only_fields = ['id', 'created_at']


class FAQSerializer(serializers.ModelSerializer):
    """FAQ serializer"""

    class Meta:
        model = FAQ
        fields = ['id', 'bot', 'question', 'answer', 'is_active', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']