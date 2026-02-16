from django.db import models
from bots.models import Bot


class Chat(models.Model):
    """
    Chat - Telegram foydalanuvchi bilan bot o'rtasidagi suhbat
    """
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='chats', verbose_name="Bot")

    # Telegram user info
    telegram_user_id = models.BigIntegerField(verbose_name="Telegram User ID")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, verbose_name="Ism")
    last_name = models.CharField(max_length=255, blank=True, verbose_name="Familiya")

    # Contact info
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    # Status
    is_blocked = models.BooleanField(default=False, verbose_name="Bloklangan")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    # Statistics
    message_count = models.IntegerField(default=0, verbose_name="Xabarlar soni")
    last_message_at = models.DateTimeField(blank=True, null=True, verbose_name="Oxirgi xabar")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
        ordering = ['-last_message_at']
        unique_together = ['bot', 'telegram_user_id']

    def __str__(self):
        name = self.first_name or self.username or f"User {self.telegram_user_id}"
        return f"{self.bot.name} - {name}"

    @property
    def full_name(self):
        """To'liq ism"""
        parts = [self.first_name, self.last_name]
        return ' '.join([p for p in parts if p])

    @property
    def display_name(self):
        """Ko'rsatish uchun ism"""
        return self.full_name or self.username or f"User {self.telegram_user_id}"