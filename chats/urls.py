from django.urls import path
from .views import (
    ChatListView,
    ChatDetailView,
    block_chat,
    delete_chat
)

app_name = 'chats'

urlpatterns = [
    path('bot/<int:bot_id>/chats/', ChatListView.as_view(), name='chat-list'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('<int:pk>/block/', block_chat, name='chat-block'),
    path('<int:pk>/delete/', delete_chat, name='chat-delete'),
]