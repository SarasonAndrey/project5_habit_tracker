from django.core.exceptions import ValidationError


def validate_related_habit_or_reward(value):
    """Проверяет, что указано либо вознаграждение, либо связанная привычка, но не оба."""
    # Эта функция будет вызываться для reward или related_habit
    # Но мы проверим это в модели через clean()
    pass


def validate_execution_time(value):
    """Время выполнения не должно превышать 120 секунд."""
    if value > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_pleasant_habit(value):
    """Приятная привычка не может иметь вознаграждение или связанную привычку."""
    # Проверяется в модели
    pass


def validate_periodicity(value):
    """Периодичность не должна быть больше 7 дней."""
    if value > 7:
        raise ValidationError("Периодичность не должна быть больше 7 дней.")
