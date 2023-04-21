import sqlite3

# Импортируйте функции из tiktok.py и youtube.py
from tiktok import upload_tiktok_video
from youtube import upload_video_to_youtube

# Замените функцию get_api_keys на get_user_credentials
def get_user_credentials(user_id):
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute('SELECT tiktok_username, tiktok_password, youtube_key FROM profiles WHERE user_id=?', (user_id,))
    result = c.fetchone()
    conn.close()

    if result:
        tiktok_username, tiktok_password, youtube_key = result
    else:
        tiktok_username, tiktok_password, youtube_key = None, None, None

    return tiktok_username, tiktok_password, youtube_key

# Внесите изменения в функцию process_age_restriction
@dp.message_handler(lambda message: message.text, state=VideoStates.age_restriction)
async def process_age_restriction(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    age_restriction = int(message.text)
    await FSMContext.update_data(user_id=user_id, age_restriction=age_restriction)

    data = await FSMContext.get_data(user_id=user_id)
    video_file_id = data["video_file_id"]
    title = data["title"]
    description = data["description"]
    tags = data["tags"]

    # Загрузка видео на TikTok и YouTube
    video_file = await bot.get_file(video_file_id)
    video_path = await video_file.download()

    tiktok_username, tiktok_password, youtube_key = get_user_credentials(user_id)

    tiktok_result = upload_tiktok_video(tiktok_username, tiktok_password, video_path, title, description, ' '.join(tags))
    youtube_result = upload_video_to_youtube(youtube_key, video_path, title, description, ', '.join(tags), age_restriction)

    response_text = f"Видео успешно опубликовано на платформах:\nTikTok: {tiktok_result}\nYouTube Shorts: {youtube_result}"
    await bot.send_message(chat_id=message.chat.id, text=response_text)
    await state.finish()
