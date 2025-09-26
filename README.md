# Habit Tracker

## Описание
Это веб-приложение помогает отслеживать полезные привычки, основываясь на методике из книги "Атомные привычки" Джеймса Клира.

## Функциональность
- Создание, редактирование и удаление привычек.
- Возможность делиться публичными привычками.
- Уведомления через Telegram.
- Автоматические напоминания.

## Технологии
- Python
- Django
- Django REST Framework
- Celery
- Redis
- Telegram Bot API
- Docker (опционально, для Redis)

## Установка
1. Клонируйте репозиторий: `git clone https://github.com/SarasonAndrey/project5_habit_tracker`
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте его: `source venv/bin/activate` (Linux/Mac) или `venv\Scripts\activate` (Windows)
4. Установите зависимости: `pip install -r requirements.txt`
5. Настройте `.env` файл (см. `.env.example`).
6. Выполните миграции: `python manage.py migrate`
7. Запустите сервер: `python manage.py runserver`

## Настройка Telegram-бота
1. Найдите @BotFather в Telegram.
2. Создайте нового бота: `/newbot`.
3. Следуйте инструкциям и получите токен.
4. Укажите токен в `.env` файле: `TELEGRAM_BOT_TOKEN=ваш_токен`.
5. Запустите Celery: `celery -A habit_tracker worker --loglevel=info --pool=solo`.

## API
API документация доступна по адресу: `http://127.0.0.1:8000/swagger/`

## Тестирование
Для запуска тестов: `python manage.py test`

## Автор
MIT