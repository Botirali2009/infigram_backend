from django.db import models
from bots.models import Bot


class DailyStats(models.Model):
    """
    Kunlik statistika
    """
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='daily_stats', verbose_name="Bot")
    date = models.DateField(verbose_name="Sana")

    # Messages
    messages_sent = models.IntegerField(default=0, verbose_name="Yuborilgan xabarlar")
    messages_received = models.IntegerField(default=0, verbose_name="Qabul qilingan xabarlar")

    # Users
    new_users = models.IntegerField(default=0, verbose_name="Yangi foydalanuvchilar")
    active_users = models.IntegerField(default=0, verbose_name="Faol foydalanuvchilar")

    # Engagement
    avg_response_time = models.FloatField(default=0.0, verbose_name="O'rtacha javob vaqti (sekund)")

    class Meta:
        verbose_name = "Kunlik statistika"
        verbose_name_plural = "Kunlik statistikalar"
        ordering = ['-date']
        unique_together = ['bot', 'date']

    def __str__(self):
        return f"{self.bot.name} - {self.date}"