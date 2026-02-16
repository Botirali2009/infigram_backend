from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet
import base64


class Bot(models.Model):
    """
    Telegram Bot
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bots',
        verbose_name="Egasi"
    )

    # Bot info
    name = models.CharField(max_length=255, verbose_name="Bot nomi")
    username = models.CharField(max_length=255, unique=True, verbose_name="Username")
    bot_id = models.BigIntegerField(unique=True, verbose_name="Bot ID")

    # Token (encrypted)
    encrypted_token = models.TextField(verbose_name="Shifrlangan token")
    webhook_secret = models.CharField(max_length=255, blank=True, verbose_name="Webhook secret")

    # Settings
    description = models.TextField(blank=True, verbose_name="Tavsif")
    welcome_message = models.TextField(blank=True, verbose_name="Xush kelibsiz xabari")
    auto_reply_enabled = models.BooleanField(default=False, verbose_name="Auto reply yoqilgan")

    # Status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('error', 'Error'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Status")

    # Statistics
    total_users = models.IntegerField(default=0, verbose_name="Foydalanuvchilar soni")
    total_messages = models.IntegerField(default=0, verbose_name="Xabarlar soni")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
    last_active = models.DateTimeField(blank=True, null=True, verbose_name="Oxirgi faollik")

    class Meta:
        verbose_name = "Bot"
        verbose_name_plural = "Botlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (@{self.username})"

    def encrypt_token(self, token):
        """Token ni shifrlash"""
        key = settings.SECRET_KEY.encode()[:32]
        key = base64.urlsafe_b64encode(key)
        cipher = Fernet(key)
        self.encrypted_token = cipher.encrypt(token.encode()).decode()

    def decrypt_token(self):
        """Token ni deshifrlash"""
        key = settings.SECRET_KEY.encode()[:32]
        key = base64.urlsafe_b64encode(key)
        cipher = Fernet(key)
        return cipher.decrypt(self.encrypted_token.encode()).decode()


class AutoReplyRule(models.Model):
    """
    Auto Reply qoidalari
    """
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='auto_replies', verbose_name="Bot")

    # Trigger
    keywords = models.TextField(verbose_name="Kalit so'zlar (vergul bilan)")  # "narx, price, qancha"

    # Response
    reply_text = models.TextField(verbose_name="Javob matni")

    # Settings
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    priority = models.IntegerField(default=0, verbose_name="Prioritet")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "Auto Reply"
        verbose_name_plural = "Auto Replies"
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.bot.name} - {self.keywords[:30]}"

    def get_keywords_list(self):
        """Kalit so'zlar listini qaytarish"""
        return [k.strip().lower() for k in self.keywords.split(',')]


class FAQ(models.Model):
    """
    FAQ - Tez-tez so'raladigan savollar
    """
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='faqs', verbose_name="Bot")

    question = models.CharField(max_length=500, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")

    # Settings
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartib")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.bot.name} - {self.question[:50]}"