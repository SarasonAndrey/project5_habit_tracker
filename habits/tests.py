from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.validators import validate_execution_time, validate_periodicity


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="12:00",
            action="Выпить стакан воды",
            is_pleasant=False,
            execution_time=60,
            is_public=True,
        )
        self.assertEqual(habit.action, "Выпить стакан воды")

    def test_execution_time_validation(self):
        habit = Habit(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            execution_time=150,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_habit_serializer(self):
        data = {
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "execution_time": 60,
            "is_public": True,
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class HabitValidatorsTest(TestCase):
    def test_validate_execution_time(self):
        with self.assertRaises(ValidationError):
            validate_execution_time(150)

    def test_validate_periodicity(self):
        with self.assertRaises(ValidationError):
            validate_periodicity(10)


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
            "execution_time": 60,
            "is_public": True,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_public_habits(self):
        Habit.objects.create(
            user=self.user,
            place="Парк",
            time="10:00",
            action="Прогулка",
            execution_time=60,
            is_public=True,
        )
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_habit(self):
        data = {
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "execution_time": 60,
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
        )
        response = self.client.get("/api/habits/")
        self.assertContains(response, "Прогулка")

    def test_create_habit_sets_user(self):
        data = {
            "place": "Дома",
            "time": "12:00",
            "action": "Приседания",
            "execution_time": 60,
            "is_public": True,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        habit = Habit.objects.get(action="Приседания")
        self.assertEqual(habit.user, self.user)
