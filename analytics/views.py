from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .models import DailyStats
from .serializers import DailyStatsSerializer
from bots.models import Bot


class DailyStatsListView(generics.ListAPIView):
    """
    Kunlik statistikalar
    GET /api/bots/{bot_id}/stats/daily/
    """
    serializer_class = DailyStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        bot_id = self.kwargs.get('bot_id')
        bot = get_object_or_404(Bot, id=bot_id, owner=self.request.user)

        # Oxirgi 30 kun
        start_date = datetime.now().date() - timedelta(days=30)
        return DailyStats.objects.filter(bot=bot, date__gte=start_date).order_by('-date')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bot_overview(request, bot_id):
    """
    Bot umumiy statistikasi
    GET /api/bots/{bot_id}/stats/overview/
    """
    bot = get_object_or_404(Bot, id=bot_id, owner=request.user)

    # Oxirgi 7 kun statistikasi
    week_ago = datetime.now().date() - timedelta(days=7)
    week_stats = DailyStats.objects.filter(bot=bot, date__gte=week_ago).aggregate(
        total_messages=Sum('messages_sent') + Sum('messages_received'),
        total_new_users=Sum('new_users'),
        avg_response_time=Sum('avg_response_time') / Count('id')
    )

    return Response({
        'bot': {
            'id': bot.id,
            'name': bot.name,
            'status': bot.status,
            'total_users': bot.total_users,
            'total_messages': bot.total_messages,
        },
        'week_stats': week_stats,
        'growth': {
            'users': '+12.5%',  # Bu real hesoblash kerak
            'messages': '+8.2%',
        }
    })