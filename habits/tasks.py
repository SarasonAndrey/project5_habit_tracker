from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.utils import send_telegram_message
from users.models import TelegramUser


@shared_task
def send_habit_reminder():
    now = timezone.now()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        try:
            chat_id = habit.user.telegram_profile.telegram_chat_id
            message = f"Напоминание: пора выполнить привычку '{habit.action}' в {habit.place}!"
            send_telegram_message(chat_id, message)
        except TelegramUser.DoesNotExist:
            pass
