# myapp/management/commands/start_telegram_bot.py
from django.core.management.base import BaseCommand
from result.telegram_bot import run_telegram_bot


class Command(BaseCommand):
    help = 'Запускает телеграм-бота'

    def handle(self, *args, **kwargs):
        run_telegram_bot()
