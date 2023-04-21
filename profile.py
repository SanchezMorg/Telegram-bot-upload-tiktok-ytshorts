import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

from main import bot, dp

class ProfileStates(StatesGroup):
    update_tiktok_username = State()
    update_tiktok_password = State()
    update_youtube = State()

def create_table():
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (user_id INTEGER PRIMARY KEY, tiktok_username TEXT, tiktok_password TEXT, youtube_key TEXT)''')
    conn.commit()
    conn.close()

create_table()

async def show_profile(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('SELECT tiktok_username, tiktok_password, youtube_key FROM profiles WHERE user_id=?', (user_id,))
    result = c.fetchone()
    conn.close()

    if result:
        tiktok_username, tiktok_password, youtube_key = result
    else:
        tiktok_username, tiktok_password, youtube_key = None, None, None

    response_text = f'Профиль:\nTikTok: {tiktok_username or "не установлен"} / {tiktok_password or "не установлен"}\nYouTube API ключ: {youtube_key or "не установлен"}'

    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Изменить данные", callback_data="update_profile"))

    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'update_profile')
async def update_profile_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await ProfileStates.update_tiktok_username.set()
    await bot.send_message(chat_id=callback_query.from_user.id, text="Пожалуйста, введите новое имя пользователя для TikTok:")

@dp.message_handler(lambda message: message.text, state=ProfileStates.update_tiktok_username)
async def update_tiktok_username(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_tiktok_username = message.text

    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO profiles (user_id, tiktok_username, tiktok_password, youtube_key) VALUES (?, ?, ?, ?)', (user_id, new_tiktok_username, None, None))
    c.execute('UPDATE profiles SET tiktok_username=? WHERE user_id=?', (new_tiktok_username, user_id))
    conn.commit()
    conn.close()

    await bot.send_message(chat_id=message.chat.id, text="Имя пользователя для TikTok обновлено. Теперь введите новый пароль для TikTok:")
    await ProfileStates.update_tiktok_password.set()

@dp.message_handler(lambda message: message.text, state=ProfileStates.update_tiktok_password)
async def update_tiktok_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_tiktok_password = message.text
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('UPDATE profiles SET tiktok_password=? WHERE user_id=?', (new_tiktok_password, user_id))
    conn.commit()
    conn.close()

    await bot.send_message(chat_id=message.chat.id, text="Пароль для TikTok обновлен. Теперь введите новый API ключ для YouTube:")
    await ProfileStates.update_youtube.set()

@dp.message_handler(lambda message: message.text, state=ProfileStates.update_youtube)
async def update_youtube_key(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    new_youtube_key = message.text
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('UPDATE profiles SET youtube_key=? WHERE user_id=?', (new_youtube_key, user_id))
    conn.commit()
    conn.close()

    await bot.send_message(chat_id=message.chat.id, text="API ключ для YouTube обновлен.")
    await show_profile(message)
    await state.finish()

async def help_with_api_keys(message: types.Message):
    response_text = "Для получения API ключей для TikTok и YouTube, пожалуйста, следуйте инструкциям на их официальных сайтах:"
    response_text += "\n\nTikTok: https://developers.tiktok.com/doc/Getting-Started"
    response_text += "\n\nYouTube: https://developers.google.com/youtube/v3/getting-started"
    await bot.send_message(chat_id=message.chat.id, text=response_text)
