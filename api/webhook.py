from fastapi import APIRouter, Request, Header, HTTPException
from aiogram import types, Dispatcher, Bot
from core.config import settings

router = APIRouter()

# Las variables dp y bot serán inyectadas o importadas desde main/bot config.
# En esta arquitectura simplificada, pasaremos la referencia en main.py,
# pero para evitar dependencias circulares, aiogram procesa directamente
# a través de una función de envoltura que se definirá aquí o en main.

async def process_update(request: Request, bot: Bot, dp: Dispatcher):
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != settings.telegram_webhook_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return {"ok": True}
