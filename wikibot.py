import asyncio
from aiogram import types, Dispatcher, Bot
from bs4 import BeautifulSoup
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote

bot = Bot(token="5401094560:AAESZEGOKDDVZJEHFele0NGeYEecMX46vr8")
dp = Dispatcher(bot)

async def fetch_url(query):
    async with aiohttp.ClientSession() as session:
        url = f"https://ru.wikipedia.org/wiki/{quote(query)}"
        async with session.get(url) as response:
            return await response.text()

def scrape_wikipedia_url(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.find("div", class_="noarticletext"):
        return None  # Страница с таким названием не существует
    return soup.find("link", rel="canonical")["href"]

async def send_wikipedia_article(message, query):
    html = await fetch_url(query)
    url = scrape_wikipedia_url(html)
    
    if url:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            driver.execute_script("window.scrollTo(0, 200)")
            screenshot = driver.get_screenshot_as_png()
            
            await bot.send_photo(
                message.chat.id,
                photo=screenshot,
                caption=f'Ссылка на статью: <a href="{url}">wiki</a>',
                parse_mode="HTML"
            )
        finally:
            driver.quit()
    else:
        await bot.send_message(message.chat.id, "Статья не найдена.")

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await message.answer("Привет")

@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    query = message.text
    await send_wikipedia_article(message, query)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()

