from django.contrib.auth.models import User
from django.db import models


class TelegramUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="telegram_profile"
    )
    telegram_chat_id = models.CharField(
        max_length=50, unique=True, verbose_name="Telegram Chat ID"
    )

    def __str__(self):
        return f"{self.user.username} - {self.telegram_chat_id}"

    class Meta:
        verbose_name = "Telegram профиль"
        verbose_name_plural = "Telegram профили"
