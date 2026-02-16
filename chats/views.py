from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Chat
from .serializers import ChatSerializer, ChatListSerializer
from bots.models import Bot


class ChatListView(generics.ListAPIView):
    """
    Chat ro'yxati
    GET /api/bots/{bot_id}/chats/
    """
    serializer_class = ChatListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        bot_id = self.kwargs.get('bot_id')
        bot = get_object_or_404(Bot, id=bot_id, owner=self.request.user)
        return Chat.objects.filter(bot=bot).order_by('-last_message_at')


class ChatDetailView(generics.RetrieveUpdateAPIView):
    """
    Chat detallari
    GET/PUT /api/chats/{id}/
    """
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(bot__owner=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def block_chat(request, pk):
    """
    Chat ni bloklash/blokdan chiqarish
    POST /api/chats/{id}/block/
    """
    chat = get_object_or_404(Chat, pk=pk, bot__owner=request.user)
    chat.is_blocked = not chat.is_blocked
    chat.save()

    return Response({
        'message': 'Muvaffaqiyatli!',
        'is_blocked': chat.is_blocked
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_chat(request, pk):
    """
    Chat ni o'chirish
    DELETE /api/chats/{id}/
    """
    chat = get_object_or_404(Chat, pk=pk, bot__owner=request.user)
    chat.delete()

    return Response({
        'message': 'Chat o\'chirildi!'
    }, status=status.HTTP_204_NO_CONTENT)