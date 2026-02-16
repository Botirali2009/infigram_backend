# bots/webhook.py
# Telegram Bot Webhook Handler

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging
from .models import Bot
from chats.models import Chat
from bot_messages.models import Message

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def telegram_webhook(request, bot_id):
    """
    Telegram webhook handler
    POST /api/webhook/{bot_id}/
    """
    try:
        # Get bot
        bot = Bot.objects.get(id=bot_id, status='active')
    except Bot.DoesNotExist:
        return HttpResponse(status=404)

    # Parse webhook data
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Handle update
    if 'message' in data:
        handle_message(bot, data['message'])

    return JsonResponse({'ok': True})


def handle_message(bot, message):
    """Handle incoming message"""
    try:
        # Get or create chat
        from_user = message.get('from', {})
        chat_data = message.get('chat', {})

        telegram_user_id = from_user.get('id')
        if not telegram_user_id:
            return

        # Get or create Chat
        chat, created = Chat.objects.get_or_create(
            bot=bot,
            telegram_user_id=telegram_user_id,
            defaults={
                'username': from_user.get('username'),
                'first_name': from_user.get('first_name', ''),
                'last_name': from_user.get('last_name', ''),
            }
        )

        # Update chat info if not created
        if not created:
            chat.username = from_user.get('username') or chat.username
            chat.first_name = from_user.get('first_name', '') or chat.first_name
            chat.last_name = from_user.get('last_name', '') or chat.last_name
            chat.save()

        # Determine message type and content
        message_type = 'text'
        text = message.get('text', '')
        file_id = None

        if 'photo' in message:
            message_type = 'photo'
            file_id = message['photo'][-1]['file_id']
        elif 'video' in message:
            message_type = 'video'
            file_id = message['video']['file_id']
        elif 'audio' in message:
            message_type = 'audio'
            file_id = message['audio']['file_id']
        elif 'voice' in message:
            message_type = 'voice'
            file_id = message['voice']['file_id']
        elif 'document' in message:
            message_type = 'document'
            file_id = message['document']['file_id']
        elif 'sticker' in message:
            message_type = 'sticker'
            file_id = message['sticker']['file_id']

        # Create message
        msg = Message.objects.create(
            chat=chat,
            telegram_message_id=message['message_id'],
            sender='user',
            message_type=message_type,
            text=text,
            file_id=file_id
        )

        # Update chat statistics
        chat.message_count += 1
        chat.last_message_at = msg.created_at
        chat.save()

        # Update bot statistics
        bot.total_messages += 1
        bot.last_active = msg.created_at
        bot.save()

        # Check for auto-reply rules
        if bot.auto_reply_enabled and text:
            check_auto_reply(bot, chat, text)

        logger.info(f"Message saved: Bot={bot.id}, Chat={chat.id}, Type={message_type}")

    except Exception as e:
        logger.error(f"Error handling message: {e}")


def check_auto_reply(bot, chat, text):
    """Check and send auto-reply if matched"""
    from .models import AutoReplyRule
    import requests

    text_lower = text.lower()

    # Get active auto-reply rules
    rules = AutoReplyRule.objects.filter(
        bot=bot,
        is_active=True
    ).order_by('-priority')

    for rule in rules:
        keywords = rule.get_keywords_list()

        # Check if any keyword matches
        if any(keyword in text_lower for keyword in keywords):
            # Send auto-reply
            token = bot.decrypt_token()
            url = f'https://api.telegram.org/bot{token}/sendMessage'

            try:
                response = requests.post(url, json={
                    'chat_id': chat.telegram_user_id,
                    'text': rule.reply_text
                })

                if response.ok:
                    data = response.json()

                    # Save bot's message
                    Message.objects.create(
                        chat=chat,
                        telegram_message_id=data['result']['message_id'],
                        sender='bot',
                        message_type='text',
                        text=rule.reply_text
                    )

                    logger.info(f"Auto-reply sent: Rule={rule.id}, Chat={chat.id}")
                    break  # Only send one auto-reply

            except Exception as e:
                logger.error(f"Error sending auto-reply: {e}")


def setup_webhook(bot):
    """Setup webhook for bot"""
    import requests

    token = bot.decrypt_token()
    webhook_url = f"https://yourdomain.com/api/webhook/{bot.id}/"

    # Set webhook
    url = f'https://api.telegram.org/bot{token}/setWebhook'

    try:
        response = requests.post(url, json={
            'url': webhook_url,
            'allowed_updates': ['message']
        })

        if response.ok:
            logger.info(f"Webhook set for bot {bot.id}")
            return True
        else:
            logger.error(f"Failed to set webhook: {response.text}")
            return False

    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return False
