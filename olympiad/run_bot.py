import os
import django
import threading
from result.telegram_bot import run_telegram_bot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olympiad.settings')
django.setup()


def start_bot():
    run_telegram_bot()


# Запуск бота в отдельном потоке
bot_thread = threading.Thread(target=start_bot, daemon=True)
bot_thread.start()
