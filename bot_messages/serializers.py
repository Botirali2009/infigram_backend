from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer"""
    chat_name = serializers.CharField(source='chat.display_name', read_only=True)
    reply_to_text = serializers.CharField(source='reply_to.text', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'chat', 'chat_name', 'telegram_message_id', 'sender',
            'message_type', 'text', 'file_id', 'file_path', 'file_size',
            'reply_to', 'reply_to_text', 'is_forwarded',
            'is_read', 'is_deleted', 'created_at'
        ]
        read_only_fields = ['id', 'telegram_message_id', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    """Xabar yuborish uchun"""

    class Meta:
        model = Message
        fields = ['chat', 'text', 'message_type', 'reply_to']