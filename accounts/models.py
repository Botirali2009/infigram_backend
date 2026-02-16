from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model
    Infigram platformasidagi foydalanuvchilar
    """
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")

    # Subscription
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('business', 'Business'),
    ]
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free', verbose_name="Plan")
    plan_expires_at = models.DateTimeField(blank=True, null=True, verbose_name="Plan tugash sanasi")

    # Statistics
    total_bots = models.IntegerField(default=0, verbose_name="Botlar soni")
    total_messages = models.IntegerField(default=0, verbose_name="Xabarlar soni")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    @property
    def is_pro(self):
        """Pro plan bormi?"""
        return self.plan in ['pro', 'business']

    @property
    def bot_limit(self):
        """Nechta bot qo'shish mumkin?"""
        limits = {
            'free': 1,
            'pro': 5,
            'business': 999999  # Unlimited
        }
        return limits.get(self.plan, 1)