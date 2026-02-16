from django.urls import path
from .webhook import telegram_webhook
from .views import (
    BotListCreateView,
    BotDetailView,
    BotStatsView,
    AutoReplyListCreateView,
    AutoReplyDetailView,
    FAQListCreateView,
    FAQDetailView
)

app_name = 'bots'

urlpatterns = [

    # ... existing urls
    path('webhook/<int:bot_id>/', telegram_webhook, name='webhook'),

    # Bot CRUD
    path('', BotListCreateView.as_view(), name='bot-list'),
    path('<int:pk>/', BotDetailView.as_view(), name='bot-detail'),
    path('<int:pk>/stats/', BotStatsView.as_view(), name='bot-stats'),

    # Auto Reply
    path('<int:bot_id>/auto-replies/', AutoReplyListCreateView.as_view(), name='auto-reply-list'),
    path('auto-replies/<int:pk>/', AutoReplyDetailView.as_view(), name='auto-reply-detail'),

    # FAQ
    path('<int:bot_id>/faqs/', FAQListCreateView.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]