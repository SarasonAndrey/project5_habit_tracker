from django.test import Client, TestCase
from django.urls import reverse


class CeleryConfigTest(TestCase):
    def test_celery_app_exists(self):
        from habit_tracker.celery import app

        self.assertIsNotNone(app)


class HabitTrackerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
