import imports
import funcs
import BusClass

bot = imports.Bot(token=imports.const.BOT_TOKEN)
dp = imports.Dispatcher()

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
    chat_id = message.chat.id
    if chat_id not in imports.const.USER_DATA or imports.const.USER_DATA[chat_id]["ischoice"] == False:
        await funcs.anti_spam(message)
        if chat_id in imports.const.IGNORE_LIST: return
        await message.reply(text='Ничего лучше не придумал???')
        await spy(message)
    else:
        if imports.const.USER_DATA[chat_id]["city"] is not None:
            if imports.const.USER_DATA[chat_id]["station"] is not None:
                if imports.const.USER_DATA[chat_id]["side"] is not None:
                    if imports.const.USER_DATA[chat_id]["bus"] is not None:
                        user = imports.const.USER_DATA[chat_id]
                        bus = BusClass.Bus(imports.const.ras, user["city"], user["station"], user["side"], user["bus"])
                        await bus.print_table()
                        length = len(bus.list_commands)
                        await bot.send_message(chat_id, bus.list_commands[-1], reply_markup=funcs.create_Inlinekeyboard(length - 1, bus.list_commands[:length - 1], inString=2, CallbackData='asdasdasd').as_markup())
                    else: await choice_bus(message)
                else: await choice_side(message)
            else: await choice_station(message)
        else: await choice_city(message)

async def start_command(message : imports.Message):
    if await funcs.anti_spam(message):
        if message.chat.id in imports.const.IGNORE_LIST: return
        await spy(message)
        await message.answer("Привет! Пока что я умею только присылать пикчи с котиками по команде /cats или /c и пикчи с аниме по команде /anime или /a", reply_markup=funcs.create_Replykeyboard(3, ['/a', '/c', '/ras'], inString=3).as_markup(resize_keyboard=True))
    else: await donothing(message)

async def cats_command(message : imports.Message) -> None:
    if await funcs.anti_spam(message):
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
    else: await donothing(message)

async def anime_command(message : imports.Message) -> None:
    if await funcs.anti_spam(message):
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
    else: await donothing(message)

async def donothing(message : imports.Message):
    pass

async def choice_city(message : imports.Message):
    await message.answer("Выберите город", reply_markup=funcs.create_Replykeyboard(len(imports.const.ras.keys()), sorted(map(str, imports.const.ras.keys())), inString=2).as_markup(resize_keyboard=True))

async def choice_station(message : imports.Message):
    pass

async def choice_side(message : imports.Message):
    pass

async def choice_bus(message : imports.Message):
    pass

async def ras_command(message : imports.Message):
    imports.const.USER_DATA[message.chat.id] = {
        "ischoice":True,
        "city":None,
        "station":None,
        "side":None,
        "bus":None
    }
    if await funcs.anti_spam(message):
        await choice_city(message)
    else: await donothing(message)
    await spy(message)

dp.message.register(start_command, imports.Command(commands=["start"]))
dp.message.register(cats_command, imports.Command(commands=["cats", "c"]))
dp.message.register(anime_command, imports.Command(commands=["anime", "a"]))
dp.message.register(ras_command, imports.Command(commands=['ras']))
dp.message.register(any_message)

if __name__ == '__main__':
    dp.run_polling(bot)