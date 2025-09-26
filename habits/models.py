from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from habits.validators import validate_execution_time, validate_periodicity


class Habit(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность (дни)"
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    execution_time = models.PositiveIntegerField(
        verbose_name="Время на выполнение (сек)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Публичная")
    execution_time = models.PositiveIntegerField(validators=[validate_execution_time])
    periodicity = models.PositiveIntegerField(validators=[validate_periodicity])

    def __str__(self):
        return f"{self.user} - {self.action} в {self.time}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        if self.execution_time > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")

        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if self.periodicity > 7:
            raise ValidationError("Периодичность не должна быть больше 7 дней.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
