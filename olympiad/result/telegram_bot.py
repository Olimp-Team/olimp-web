# telegram_bot.py
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from users.models import User
from result.models import Result
from asgiref.sync import sync_to_async

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Токен вашего бота из BotFather
TELEGRAM_TOKEN = '7320753031:AAENatl1RNNiE_JZIchsL8rNx_wd8zf4PmU'

# Словарь для временного хранения email пользователя до подтверждения
TEMP_EMAIL_STORE = {}


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Для подключения аккаунта используй команду /connect <ваш email>.')


async def connect(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Использование: /connect <ваш email>')
        return

    email = context.args[0]
    TEMP_EMAIL_STORE[update.message.from_user.id] = email
    await update.message.reply_text(f'Email {email} сохранен. Пожалуйста, подтвердите с помощью команды /confirm.')


async def confirm(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in TEMP_EMAIL_STORE:
        await update.message.reply_text('Сначала используйте команду /connect <ваш email>.')
        return

    email = TEMP_EMAIL_STORE.pop(user_id)
    user = await sync_to_async(User.objects.get)(email=email)

    if user:
        user.telegram_id = str(user_id)
        await sync_to_async(user.save)()
        await update.message.reply_text('Ваш аккаунт успешно подключен.')
    else:
        await update.message.reply_text('Пользователь с таким email не найден.')


async def send_result_update(result: Result) -> None:
    bot = Bot(token=TELEGRAM_TOKEN)
    user = await sync_to_async(result.student)()
    if user.telegram_id:
        message = f'Результат обновлен: {result.subject} - {result.score}'
        await bot.send_message(chat_id=user.telegram_id, text=message)


def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('connect', connect))
    application.add_handler(CommandHandler('confirm', confirm))

    application.run_polling()
