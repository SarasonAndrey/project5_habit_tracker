from rest_framework import serializers
from habits.validators import validate_execution_time, validate_periodicity
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_execution_time(self, value):
        validate_execution_time(value)
        return value

    def validate_periodicity(self, value):
        validate_periodicity(value)
        return value
