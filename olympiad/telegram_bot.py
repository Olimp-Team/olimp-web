import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters
import requests
from django.conf import settings
import django
import os

# Установите настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olympiad.settings')
django.setup()

from users.models import User  # Импортируйте вашу модель пользователя

# Включите логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен вашего бота
TOKEN = '7320753031:AAENatl1RNNiE_JZIchsL8rNx_wd8zf4PmU'

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте свой Telegram ID в формате "/set_id <ваш_telegram_id>"')

# Команда /set_id для установки Telegram ID пользователя
def set_telegram_id(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    telegram_id = user.id
    user_id = update.message.text.split()[1]

    try:
        # Найдите пользователя по ID и обновите его Telegram ID
        user = User.objects.get(id=user_id)
        user.telegram_id = telegram_id
        user.save()
        update.message.reply_text(f'Telegram ID успешно установлен для пользователя {user.username}')
    except User.DoesNotExist:
        update.message.reply_text('Пользователь с таким ID не найден.')

# Основная функция для запуска бота
def main() -> None:
    # Создайте объект Updater и передайте ему токен вашего бота и use_context=True
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set_id", set_telegram_id))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
