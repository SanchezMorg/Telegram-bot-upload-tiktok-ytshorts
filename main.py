import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

from config import TOKEN
import bot_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, on_startup=bot_handlers.on_startup, on_shutdown=bot_handlers.on_shutdown)
