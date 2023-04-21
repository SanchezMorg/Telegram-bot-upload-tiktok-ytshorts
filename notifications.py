from aiogram import types

from main import bot

async def send_notification(chat_id, message_text):
    await bot.send_message(chat_id=chat_id, text=message_text)
