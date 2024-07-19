from django.apps import AppConfig


class ResultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'result'

    # def ready(self):
    #     import result.signals
    #     from result.telegram_bot import run_telegram_bot
    #     import asyncio
    #     asyncio.run(run_telegram_bot())
