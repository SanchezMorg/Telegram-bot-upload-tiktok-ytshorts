from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from aiogram.utils.markdown import text, quote_html

from main import bot, dp
import profile
import video_upload

@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await profile.show_profile(message)

@dp.message_handler(lambda message: message.text == "Профиль")
async def show_profile(message: types.Message):
    await profile.show_profile(message)

@dp.message_handler(lambda message: message.text == "Изменить данные")
async def update_profile(message: types.Message):
    await profile.update_profile(message)

@dp.message_handler(lambda message: message.text == "Помощь по API ключам")
async def help_with_api_keys(message: types.Message):
    await profile.help_with_api_keys(message)

@dp.message_handler(lambda message: message.text == "Выгрузить видео")
async def upload_video(message: types.Message):
    await video_upload.upload_video(message)

@dp.message_handler(content_types=types.ContentType.VIDEO)
async def process_video(message: types.Message, state: FSMContext):
    await video_upload.process_video(message, state)

async def on_startup(dp):
    await bot.send_message(chat_id=YOUR_CHAT_ID, text="Бот запущен")

async def on_shutdown(dp):
    await bot.send_message(chat_id=YOUR_CHAT_ID, text="Бот остановлен")
