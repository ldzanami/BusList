import imports

bot = imports.Bot(token=imports.const.BOT_TOKEN)
dp = imports.Dispatcher()

def create_keyboard(how_much : int, texts : list[str], inString=1) -> imports.ReplyKeyboardBuilder:
    builder = imports.ReplyKeyboardBuilder()
    for i in range(how_much):
        builder.add(imports.KeyboardButton(text=texts[i]))
    builder.adjust(inString)
    return builder

async def spy(message : imports.Message, pic=None) -> None:
    nick = message.from_user
    chatID = message.chat.id
    if message.chat.id in imports.const.IGNORE_LIST: return
    if chatID == imports.const.MY_ID: return
    if nick.username is not None:
        nick = nick.username
    else:
        nick = f'{nick.first_name} {nick.last_name}'
    ans = f'''nickname: {nick}
chatID: {chatID}
picture: {pic}'''
    await bot.send_message(imports.const.MY_ID, ans)
    try:
        await message.send_copy(chat_id=imports.const.MY_ID)
    except TypeError:
        await message.reply(text='Я даже не знаю как на это реагировать...')

async def any_message(message : imports.Message) -> None:
    if message.chat.id in imports.const.IGNORE_LIST: return
    await message.reply(text='Ничего лучше не придумал???')
    await spy(message)

async def start_command(message : imports.Message):
    if message.chat.id in imports.const.IGNORE_LIST: return
    await spy(message)
    await message.answer("Привет! Пока что я умею только присылать пикчи с котиками по команде /cats или /c и пикчи с аниме по команде /anime или /a", reply_markup=create_keyboard(2, ['/a', '/c'], inString=2).as_markup(resize_keyboard=True))

async def cats_command(message : imports.Message) -> None:
    if message.chat.id in imports.const.IGNORE_LIST: return
    ans = imports.requests.get(imports.const.API_CATS_URL)
    if ans.status_code == 200:
        pic = ans.json()[0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except imports.aiogram.exceptions.TelegramBadRequest:
            await message.answer(imports.const.FAIL_ANS)
            if message.from_user.id != imports.const.MY_ID:
                await bot.send_message(imports.const.MY_ID, imports.const.FAIL_ANS + str(message.from_user.first_name))
    else:
        await message.answer(ans.status_code)

async def anime_command(message : imports.Message) -> None:
    if message.chat.id in imports.const.IGNORE_LIST: return
    ans = imports.requests.get(imports.const.API_WAIFU_URL)
    if ans.status_code == 200:
        pic = ans.json()['images'][0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except imports.aiogram.exceptions.TelegramBadRequest:
            await message.answer(imports.const.FAIL_ANS)
            if message.from_user.id != imports.const.MY_ID:
                await bot.send_message(imports.const.MY_ID, f"{message.from_user.first_name} {imports.const.FAIL_ANS}")
    else:
        await message.answer(ans.status_code)

def donothing(message : imports.Message):
    if message.chat.id in imports.const.IGNORE_LIST: return
    print("апдейт")

dp.message.register(start_command, imports.Command(commands=["start"]))
dp.message.register(cats_command, imports.Command(commands=["cats", "c"]))
dp.message.register(anime_command, imports.Command(commands=["anime", "a"]))
dp.message.register(any_message)

if __name__ == '__main__':
    dp.run_polling(bot)