from unittest.mock import patch

from django.test import TestCase

from telegram_bot.tasks import send_habit_reminder


class TelegramUtilsTest(TestCase):
    @patch("telegram_bot.utils.requests.post")
    def test_send_telegram_message(self, mock_post):
        from telegram_bot.utils import send_telegram_message

        mock_post.return_value.json.return_value = {"ok": True}
        result = send_telegram_message("123456789", "Test message")
        self.assertEqual(result["ok"], True)


def test_send_habit_reminder_no_error(self):
    send_habit_reminder()  # просто вызываем, чтобы убедиться, что не падает
    self.assertTrue(True)
