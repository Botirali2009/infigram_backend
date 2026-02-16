from django.urls import path
from .views import (
    DailyStatsListView,
    bot_overview
)

app_name = 'analytics'

urlpatterns = [
    path('bot/<int:bot_id>/daily/', DailyStatsListView.as_view(), name='daily-stats'),
    path('bot/<int:bot_id>/overview/', bot_overview, name='bot-overview'),
]