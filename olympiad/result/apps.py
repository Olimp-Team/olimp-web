from django.apps import AppConfig


class ResultConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'result'

    def ready(self):
        import result.signals
        from result.telegram_bot import main as telegram_bot_main
        import asyncio
        asyncio.run(telegram_bot_main())
