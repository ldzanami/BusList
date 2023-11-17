from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import aiogram
import requests

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '6416264890:AAHOB38AT9IESfOC-decd5NjcO_n-uipURQ'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_WAIFU_URL = 'https://api.waifu.im/search'
MY_ID = 1288933234

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def spy(message : Message, pic=None):
    nick = message.from_user
    chatID = nick.id
    if chatID == MY_ID: return
    mes = message.text
    if nick.username is not None:
        nick = nick.username
    else:
        nick = f'{nick.first_name} {nick.last_name}'
    ans = f'''nickname: {nick}
chatID: {chatID}
message: {mes}
picture: {pic}'''
    await bot.send_message(MY_ID, ans)

@dp.message(Command(commands=["start"]))
async def start_command(message : Message):
    await spy(message)
    await message.answer("Привет! Пока что я умею только присылать пикчи с котиками по команде /cats или /c и пикчи с аниме по команде /anime или /a")
@dp.message(Command(commands=["cats", "c"]))
async def cats_command(message : Message):
    ans = requests.get(API_CATS_URL)
    if ans.status_code == 200:
        pic = ans.json()[0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except aiogram.exceptions.TelegramBadRequest:
            anime_command(message)
    else:
        await message.answer(ans.status_code)
@dp.message(Command(commands=["anime", "a"]))
async def anime_command(message : Message):
    ans = requests.get(API_WAIFU_URL)
    if ans.status_code == 200:
        pic = ans.json()['images'][0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except aiogram.exceptions.TelegramBadRequest:
            anime_command(message)
    else:
        await message.answer(ans.status_code)
@dp.message()
async def any_message(message : Message):
    await spy(message)

if __name__ == '__main__':
    dp.run_polling(bot) 