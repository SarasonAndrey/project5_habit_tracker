from celery import shared_task

from telegram_bot.utils import send_telegram_message

from .models import Habit


@shared_task
def send_habit_reminder():
    """
    Отправляет уведомления о привычках, которые нужно выполнить сейчас.
    """
    habits = Habit.objects.all()
    for habit in habits:
        message = f"Не забудь: {habit.action} в {habit.time} в {habit.place}!"
        send_telegram_message(habit.user.telegram_chat_id, message)
