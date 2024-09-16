import logging
import datetime
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.ext import JobQueue
import httpx

# Настройки
TOKEN = '7420449985:AAHVJSWeVstT2kXWh1MPhGi8eGbr4vfA3h0'
NFT_COLLECTION_API = 'https://api.pallet.exchange/api/v2/nfts/sei17atqkdaqhwg3et5pr73wc7k2tv0h0httgrmx58hdwk764yf9jc9sp9ldhc/details'
BASE_IPFS_URL = 'ipfs://bafybeifboxxuol57cwhg5iagygbxbq7ufe4xbiqe2ttp4xxhtjp7bjylvi/'

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Хранилище пользователей
user_ids = set()

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_ids.add(user_id)
    await update.message.reply_text("You've been registered for daily Ghoons!")

async def fetch_random_ghoon():
    async with httpx.AsyncClient() as client:
        response = await client.get(NFT_COLLECTION_API)
        data = response.json()
        
        # Предположим, что `data` содержит список объектов NFT в поле `nfts`
        if 'nfts' not in data or not data['nfts']:
            return {
                "image_url": "https://example.com/default_image.png",  # Замените на изображение по умолчанию
                "message": "No Ghoon available today!"
            }
        
    # Функция для получения случайного NFT
async def fetch_random_ghoon():
    # Выбираем случайное число от 1 до 1107
    random_id = random.randint(1, 1107)
    
    # Формируем URL изображения на основе случайного ID
    image_url = f'https://ipfs.io/ipfs/bafybeifboxxuol57cwhg5iagygbxbq7ufe4xbiqe2ttp4xxhtjp7bjylvi/{random_id}.png'
    
    message = "This Ghoon brings happiness today!"
    
    return {
        "image_url": image_url,
        "message": message
    }

async def send_daily_ghoon(context: CallbackContext):
    for user_id in user_ids:
        ghoon = await fetch_random_ghoon()
        image_url = ghoon['image_url']
        message = f"This is your Ghoons for today! {ghoon['message']}"
        
        await context.bot.send_photo(chat_id=user_id, photo=image_url, caption=message)

def main():
    # Создание объекта Application
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчика команд /start
    application.add_handler(CommandHandler("start", start))

    # Получение JobQueue
    job_queue = application.job_queue
    
    if job_queue is None:
        logging.error("JobQueue is not available. Please make sure `python-telegram-bot[job-queue]` is installed.")
        return

    # Планирование ежедневного задания
    job_queue.run_daily(send_daily_ghoon, time=datetime.time(hour=9, minute=0, second=0))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
