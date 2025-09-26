from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from .models import Habit
from .serializers import HabitSerializer


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="12:00",
            action="Приседания",
            is_pleasant=False,
            execution_time=60,
            periodicity=1,
            is_public=True,
        )
        self.assertEqual(habit.action, "Приседания")
        self.assertEqual(habit.user, self.user)

    def test_execution_time_validation(self):
        habit = Habit(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            execution_time=150,  # больше 120 — ошибка
            periodicity=1,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_periodicity_validation(self):
        habit = Habit(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            execution_time=60,
            periodicity=10,  # больше 7 — ошибка
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_cannot_have_reward_or_related_habit(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="12:00",
            action="Выпить чай",
            is_pleasant=True,
            execution_time=60,
            periodicity=1,
        )
        habit_with_reward = Habit(
            user=self.user,
            place="Дома",
            time="13:00",
            action="Чтение",
            is_pleasant=False,
            reward="Награда",
            execution_time=60,
            periodicity=1,
        )
        habit_with_reward.related_habit = pleasant_habit
        with self.assertRaises(ValidationError):
            habit_with_reward.full_clean()

    def test_related_habit_must_be_pleasant(self):
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="12:00",
            action="Приседания",
            is_pleasant=False,
            execution_time=60,
            periodicity=1,
        )
        habit = Habit(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            related_habit=not_pleasant_habit,
            execution_time=60,
            periodicity=1,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_cannot_have_both_reward_and_related_habit(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="12:00",
            action="Выпить чай",
            is_pleasant=True,
            execution_time=60,
            periodicity=1,
        )
        habit = Habit(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            reward="Награда",
            related_habit=pleasant_habit,
            execution_time=60,
            periodicity=1,
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_habit_serializer_valid_data(self):
        data = {
            "user": self.user.id,
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "is_pleasant": False,
            "execution_time": 60,
            "periodicity": 1,
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_habit_serializer_invalid_execution_time(self):
        data = {
            "user": self.user.id,
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "is_pleasant": False,
            "execution_time": 150,  # больше 120
            "periodicity": 1,
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("execution_time", serializer.errors)

    def test_habit_serializer_invalid_periodicity(self):
        data = {
            "user": self.user.id,
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "is_pleasant": False,
            "execution_time": 60,
            "periodicity": 10,  # больше 7
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("periodicity", serializer.errors)


class HabitAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_authenticate(user=self.user)

    def test_create_habit_via_api(self):
        data = {
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "is_pleasant": False,
            "execution_time": 60,
            "periodicity": 1,
            "is_public": True,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_get_user_habits(self):
        Habit.objects.create(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            execution_time=60,
            periodicity=1,
        )
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Прогулка")

    def test_get_public_habits(self):
        Habit.objects.create(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            execution_time=60,
            periodicity=1,
            is_public=True,
        )
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Прогулка")

    def test_create_habit_sets_user(self):
        data = {
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "is_pleasant": False,
            "execution_time": 60,
            "periodicity": 1,
            "is_public": True,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit = Habit.objects.get(action="Приседания")
        self.assertEqual(habit.user, self.user)
