from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
import requests
from .models import Bot, AutoReplyRule, FAQ
from .serializers import (
    BotSerializer,
    BotCreateSerializer,
    AutoReplyRuleSerializer,
    FAQSerializer
)


class BotListCreateView(generics.ListCreateAPIView):
    """
    Bot ro'yxati va yaratish
    GET/POST /api/bots/
    """
    serializer_class = BotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bot.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        # BotCreateSerializer dan foydalanamiz
        serializer = BotCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        name = serializer.validated_data['name']
        description = serializer.validated_data.get('description', '')

        # Telegram Bot API dan bot ma'lumotlarini olish
        try:
            response = requests.get(f'https://api.telegram.org/bot{token}/getMe')
            data = response.json()

            if not data['ok']:
                return Response({
                    'error': 'Noto\'g\'ri bot token!'
                }, status=status.HTTP_400_BAD_REQUEST)

            bot_info = data['result']

            # Bot yaratish
            bot = Bot.objects.create(
                owner=request.user,
                name=name,
                username=bot_info['username'],
                bot_id=bot_info['id'],
                description=description
            )
            bot.encrypt_token(token)
            bot.save()

            # User statistikasini yangilash
            request.user.total_bots += 1
            request.user.save()

            return Response(
                BotSerializer(bot).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class BotDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Bot detallari
    GET/PUT/DELETE /api/bots/{id}/
    """
    serializer_class = BotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bot.objects.filter(owner=self.request.user)


class BotStatsView(generics.RetrieveAPIView):
    """
    Bot statistikasi
    GET /api/bots/{id}/stats/
    """
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        bot = get_object_or_404(Bot, pk=pk, owner=request.user)

        # Statistikani hisoblash
        from chats.models import Chat
        from bot_messages.models import Message

        total_chats = Chat.objects.filter(bot=bot).count()
        active_chats = Chat.objects.filter(bot=bot, is_active=True).count()
        total_messages = Message.objects.filter(chat__bot=bot).count()

        return Response({
            'bot': BotSerializer(bot).data,
            'stats': {
                'total_chats': total_chats,
                'active_chats': active_chats,
                'total_messages': total_messages,
                'total_users': bot.total_users,
            }
        })


# Auto Reply Views
class AutoReplyListCreateView(generics.ListCreateAPIView):
    """
    Auto reply ro'yxati va yaratish
    GET/POST /api/bots/{bot_id}/auto-replies/
    """
    serializer_class = AutoReplyRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        bot_id = self.kwargs.get('bot_id')
        return AutoReplyRule.objects.filter(
            bot_id=bot_id,
            bot__owner=self.request.user
        )


class AutoReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Auto reply detallari
    GET/PUT/DELETE /api/auto-replies/{id}/
    """
    serializer_class = AutoReplyRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AutoReplyRule.objects.filter(bot__owner=self.request.user)


# FAQ Views
class FAQListCreateView(generics.ListCreateAPIView):
    """
    FAQ ro'yxati va yaratish
    GET/POST /api/bots/{bot_id}/faqs/
    """
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        bot_id = self.kwargs.get('bot_id')
        return FAQ.objects.filter(
            bot_id=bot_id,
            bot__owner=self.request.user
        )


class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    FAQ detallari
    GET/PUT/DELETE /api/faqs/{id}/
    """
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FAQ.objects.filter(bot__owner=self.request.user)