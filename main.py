import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from core.config import settings
from api.health import router as health_router
from api.webhook import process_update
from bot.routers import setup_routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración del bot
bot = Bot(
    token=settings.telegram_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
setup_routers(dp)

WEBHOOK_PATH = f"/webhook/{settings.telegram_bot_token}"
WEBHOOK_URL = f"{settings.app_base_url}{WEBHOOK_PATH}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Configurando webhook...")
    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=settings.telegram_webhook_secret,
            allowed_updates=dp.resolve_used_update_types()
        )
        logger.info("Webhook configurado exitosamente con Telegram.")
    except Exception as e:
        logger.error(f"¡ERROR FATAL AL CONFIGURAR WEBHOOK!: {e}")
        logger.error("El bot encenderá, pero Telegram no le enviará mensajes hasta corregir esto.")
    yield
    logger.info("Eliminando webhook...")
    try:
        await bot.delete_webhook()
    except:
        pass
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

app.include_router(health_router)

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    return await process_update(request, bot, dp)
