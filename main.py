from dotenv import load_dotenv
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis # ассинхронная версия
import os
from contextlib import asynccontextmanager
from config import settings
from handlers import menu, info, booking

load_dotenv()
BOT_TOKEN = settings.bot_token
REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port
REDIS_PASSWORD = settings.redis_password
WEBHOOK_SECRET = settings.webhook_secret
bot = Bot(token=BOT_TOKEN)

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
storage = RedisStorage(redis=redis)

dp = Dispatcher(storage=storage)

dp.include_router(menu.router)
dp.include_router(info.router)
dp.include_router(booking.router)


async def lifespan(app):
    webhook_url = os.getenv("WEBHOOK_URL")
    try:
        await bot.set_webhook(url=webhook_url,
                            secret_token=WEBHOOK_SECRET, 
                            drop_pending_updates=True, # НЕ отвечает на старые сообщения, которые проигнорировал
                            allowed_updates=["calback_query", "message"]) # Только с ними работаю, если появится оплата, то добавлю
        print(f"Webhook установлен на {webhook_url}")
    except Exception as e:
        print(f"Ошибка установки вебхука. {e}")

    yield

    await bot.session.close()  
    await redis.aclose()  # redis.asyncio >= 5.0
    print("🔄 Webhook удален")

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def set_webhook(request: Request):
    # Получаем JSON-данные от Telegram
    json_data = await request.json()
    #Превращаем их в объект Update (тип из aiogram)
    update = types.Update(**json_data)
    # Передаём обновление диспетчеру, чтобы он нашёл нужный обработчик
    await dp.feed_update(bot, update)
    # Отвечаем Telegram, что всё приняли
    return {"ok": True}

@app.get("/webhook")
async def webhook():
    return {"status": "ok", "message" : "Webhook endpoint. Use POST for updates"}

@app.get("/ping")
async def ping():
    # Получаем информацию о текущем вебхуке
    webhook_info = await bot.get_webhook_info()
    expected_url = settings.webhook_url

    if webhook_info.url != expected_url:
        await bot.delete_webhook()
        await bot.set_webhook(url=expected_url)
        return {
            "status": "webhook_update",
            "old url": webhook_info,
            "new url": expected_url
        }
    # Всё в порядке
    return {"status" : "ok", "webhook_url" : webhook_info.url}