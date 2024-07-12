# telegram_bot.py
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from django.conf import settings
from result.models import Result

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен вашего бота из BotFather
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Хранилище пользователей
USER_STORE = {}


async def start(update: Update, context: CallbackContext) -> None:
    USER_STORE[update.message.from_user.id] = update.message.chat_id
    await update.message.reply_text('Привет! Теперь ты будешь получать уведомления о результатах.')


async def send_result_update(result: Result) -> None:
    for user_id, chat_id in USER_STORE.items():
        message = f'Результат обновлен: {result.info_olympiad} - {result.points} - {result.status_result}'
        await context.bot.send_message(chat_id=chat_id, text=message)


async def main() -> None:
    # Создаем бота
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Обработчики команд
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Запуск бота
    await application.run_polling()


if __name__ == '__main__':
    main()
