from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
    """Chat serializer"""
    bot_name = serializers.CharField(source='bot.name', read_only=True)
    display_name = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Chat
        fields = [
            'id', 'bot', 'bot_name', 'telegram_user_id', 'username',
            'first_name', 'last_name', 'full_name', 'display_name',
            'phone', 'email', 'is_blocked', 'is_active',
            'message_count', 'last_message_at', 'created_at'
        ]
        read_only_fields = ['id', 'message_count', 'last_message_at', 'created_at']


class ChatListSerializer(serializers.ModelSerializer):
    """Chat list uchun (qisqaroq)"""
    display_name = serializers.CharField(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            'id', 'telegram_user_id', 'display_name', 'username',
            'message_count', 'last_message', 'unread_count',
            'last_message_at', 'is_blocked'
        ]

    def get_last_message(self, obj):
        """Oxirgi xabar"""
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'text': last_msg.text[:50] if last_msg.text else f"[{last_msg.message_type}]",
                'sender': last_msg.sender,
                'created_at': last_msg.created_at
            }
        return None

    def get_unread_count(self, obj):
        """O'qilmagan xabarlar soni"""
        return obj.messages.filter(is_read=False, sender='user').count()