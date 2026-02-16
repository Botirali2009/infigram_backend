from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer
from chats.models import Chat
import requests


class MessageListView(generics.ListAPIView):
    """
    Xabarlar ro'yxati
    GET /api/chats/{chat_id}/messages/
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, id=chat_id, bot__owner=self.request.user)
        return Message.objects.filter(chat=chat, is_deleted=False).order_by('created_at')


class MessageSendView(generics.CreateAPIView):
    """
    Xabar yuborish
    POST /api/messages/send/
    """
    serializer_class = MessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat = serializer.validated_data['chat']
        text = serializer.validated_data['text']

        # Bot tokenini olish
        bot = chat.bot
        token = bot.decrypt_token()

        # Telegram API orqali xabar yuborish
        try:
            url = f'https://api.telegram.org/bot{token}/sendMessage'
            payload = {
                'chat_id': chat.telegram_user_id,
                'text': text
            }

            response = requests.post(url, json=payload)
            data = response.json()

            if data['ok']:
                # Xabarni DB ga saqlash
                message = Message.objects.create(
                    chat=chat,
                    telegram_message_id=data['result']['message_id'],
                    sender='bot',
                    message_type='text',
                    text=text
                )

                # Chat statistikasini yangilash
                chat.message_count += 1
                chat.last_message_at = message.created_at
                chat.save()

                return Response(
                    MessageSerializer(message).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({
                    'error': 'Xabar yuborilmadi!'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_as_read(request, pk):
    """
    Xabarni o'qilgan deb belgilash
    POST /api/messages/{id}/read/
    """
    message = get_object_or_404(Message, pk=pk, chat__bot__owner=request.user)
    message.is_read = True
    message.save()

    return Response({
        'message': 'O\'qilgan deb belgilandi!'
    })