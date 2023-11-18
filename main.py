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
FAIL_ANS = 'Что-то пошло не так и это что-то точно не в моём ботике'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def spy(message : Message, pic=None):
    nick = message.from_user
    chatID = message.chat.id
    if chatID == MY_ID: return
    if nick.username is not None:
        nick = nick.username
    else:
        nick = f'{nick.first_name} {nick.last_name}'
    ans = f'''nickname: {nick}
chatID: {chatID}
picture: {pic}'''
    await bot.send_message(MY_ID, ans)
    try:
        await message.send_copy(chat_id=MY_ID)
    except TypeError:
        await message.reply(text='Я даже не знаю как на это реагировать...')

async def any_message(message : Message):
    await message.reply(text='Ничего лучше не придумал???')
    await spy(message)

async def start_command(message : Message):
    await spy(message)
    await message.answer("Привет! Пока что я умею только присылать пикчи с котиками по команде /cats или /c и пикчи с аниме по команде /anime или /a")

async def cats_command(message : Message):
    ans = requests.get(API_CATS_URL)
    if ans.status_code == 200:
        pic = ans.json()[0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except aiogram.exceptions.TelegramBadRequest:
            await message.answer(FAIL_ANS)
            if message.from_user.id != MY_ID:
                await bot.send_message(MY_ID, FAIL_ANS + str(message.from_user.first_name))
    else:
        await message.answer(ans.status_code)

async def anime_command(message : Message):
    ans = requests.get(API_WAIFU_URL)
    if ans.status_code == 200:
        pic = ans.json()['images'][0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except aiogram.exceptions.TelegramBadRequest:
            await message.answer(FAIL_ANS)
            if message.from_user.id != MY_ID:
                await bot.send_message(MY_ID, f"{message.from_user.first_name} {FAIL_ANS}")
    else:
        await message.answer(ans.status_code)

dp.message.register(start_command, Command(commands=["start"]))
dp.message.register(cats_command, Command(commands=["cats", "c"]))
dp.message.register(anime_command, Command(commands=["anime", "a"]))
dp.message.register(any_message)

if __name__ == '__main__':
    dp.run_polling(bot) 