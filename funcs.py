import imports
import Buttons

async def spy(message : imports.Message, pic=None):
    nick = message.from_user
    chatID = message.chat.id
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

async def any_message(message : imports.Message):
    await message.reply(text='Ничего лучше не придумал???')
    await spy(message)

async def start_command(message : imports.Message):
    await spy(message)
    await message.answer("Привет! Пока что я умею только присылать пикчи с котиками по команде /cats или /c и пикчи с аниме по команде /anime или /a", reply_markup=Buttons.keyboard)

async def cats_command(message : imports.Message):
    ans = imports.requests.get(imports.const.API_CATS_URL)
    if ans.status_code == 200:
        pic = ans.json()[0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except imports.aiogram.exceptions.TelegramBadRequest:
            await message.answer(FAIL_ANS)
            if message.from_user.id != imports.const.MY_ID:
                await bot.send_message(imports.const.MY_ID, FAIL_ANS + str(message.from_user.first_name))
    else:
        await message.answer(ans.status_code)

async def anime_command(message : imports.Message):
    ans = imports.requests.get(imports.const.API_WAIFU_URL)
    if ans.status_code == 200:
        pic = ans.json()['images'][0]["url"]
        try:
            await spy(message, pic=pic)
            await message.answer_photo(pic)
        except imports.aiogram.exceptions.TelegramBadRequest:
            await message.answer(FAIL_ANS)
            if message.from_user.id != imports.const.MY_ID:
                await bot.send_message(imports.const.MY_ID, f"{message.from_user.first_name} {FAIL_ANS}")
    else:
        await message.answer(ans.status_code)