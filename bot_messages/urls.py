from django.urls import path
from .views import (
    MessageListView,
    MessageSendView,
    mark_as_read
)

app_name = 'bot_messages'

urlpatterns = [
    path('chat/<int:chat_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('send/', MessageSendView.as_view(), name='message-send'),
    path('<int:pk>/read/', mark_as_read, name='message-read'),
]