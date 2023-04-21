import asyncio
from pyppeteer import launch
from pyppeteer.errors import NetworkError, TimeoutError

async def login(page, username, password):
    await page.goto("https://www.tiktok.com/login")
    await asyncio.sleep(2)

    # Введите имя пользователя и пароль
    await page.type('input[name="username"]', username)
    await page.type('input[name="password"]', password)
    await asyncio.sleep(1)

    # Нажмите кнопку входа
    await page.click('button[type="submit"]')
    await asyncio.sleep(5)

async def upload_video(username, password, video_path, title, description, tags):
    browser = await launch(headless=False)
    page = await browser.newPage()

    await login(page, username, password)

    try:
        await page.waitForSelector('input[type="file"]', timeout=10000)
        input_file = await page.querySelector('input[type="file"]')
        await input_file.uploadFile(video_path)
        await asyncio.sleep(5)

        await page.type('input[placeholder="Write a caption..."]', f'{title}\n{description}\n{tags}')
        await asyncio.sleep(1)

        await page.click('button[type="submit"]')
        await asyncio.sleep(5)
    except (NetworkError, TimeoutError):
        print("Не удалось загрузить видео.")
    finally:
        await browser.close()

def upload_tiktok_video(username, password, video_path, title, description, tags):
    asyncio.get_event_loop().run_until_complete(upload_video(username, password, video_path, title, description, tags))
