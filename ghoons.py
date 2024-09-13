import logging
import random
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.ext import JobQueue
import requests

# Настройки
TOKEN = '7420449985:AAHVJSWeVstT2kXWh1MPhGi8eGbr4vfA3h0'
NFT_COLLECTION_API = 'https://api.pallet.exchange/api/v2/nfts/sei17atqkdaqhwg3et5pr73wc7k2tv0h0httgrmx58hdwk764yf9jc9sp9ldhc/details'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Хранилище пользователей
user_ids = set()

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_ids.add(user_id)
    update.message.reply_text("You've been registered for daily Ghoons!")

def fetch_random_ghoon():
    response = requests.get(NFT_COLLECTION_API)
    data = response.json()
    # Для упрощения возьмем первый элемент из списка traits
    ghoon = {
        "image_url": data['image_url'],
        "message": data['message']
    }
    return ghoon

def send_daily_ghoon(context: CallbackContext):
    for user_id in user_ids:
        ghoon = fetch_random_ghoon()
        image_url = ghoon['image_url']
        message = f"This is your Ghoons for today! {ghoon['message']}"
        
        context.bot.send_photo(chat_id=user_id, photo=image_url, caption=message)

def main():
    # Создание объекта Application
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчика команд /start
    application.add_handler(CommandHandler("start", start))

    # Получение JobQueue
    job_queue = application.job_queue

    # Планирование ежедневного задания
    job_queue.run_daily(send_daily_ghoon, time=datetime.time(hour=9, minute=0, second=0))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
