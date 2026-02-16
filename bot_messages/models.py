from django.db import models
from chats.models import Chat


class Message(models.Model):
    """
    Message - Bot va foydalanuvchi o'rtasidagi xabar
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name="Chat")

    # Message info
    telegram_message_id = models.BigIntegerField(verbose_name="Telegram Message ID")

    # Sender
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Yuboruvchi")

    # Content
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('voice', 'Voice'),
        ('document', 'Document'),
        ('sticker', 'Sticker'),
        ('location', 'Location'),
        ('contact', 'Contact'),
    ]
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text',
                                    verbose_name="Xabar turi")

    text = models.TextField(blank=True, verbose_name="Matn")

    # File info
    file_id = models.CharField(max_length=255, blank=True, verbose_name="File ID")
    file_path = models.CharField(max_length=500, blank=True, verbose_name="File path")
    file_size = models.BigIntegerField(blank=True, null=True, verbose_name="File hajmi")

    # Reply/Forward info
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='replies',
        verbose_name="Javob"
    )
    is_forwarded = models.BooleanField(default=False, verbose_name="Forward qilingan")

    # Status
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    is_deleted = models.BooleanField(default=False, verbose_name="O'chirilgan")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['chat', 'created_at']),
            models.Index(fields=['telegram_message_id']),
        ]

    def __str__(self):
        preview = self.text[:50] if self.text else f"[{self.message_type}]"
        return f"{self.chat.display_name} - {preview}"