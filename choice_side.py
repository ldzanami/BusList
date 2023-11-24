from FSMClass import FSMChoiceBus
import funcs

async def choice_side(message, state, ras, USER_DATA, ADMINS, ads):
    user = USER_DATA[message.from_user.id]
    rass = ras[user["city"]][user['station']]
    if message.text in rass:
        USER_DATA[message.from_user.id]['side'] = message.text
        # print(USER_DATA)
        await state.set_state(FSMChoiceBus.choice_bus)
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Выберите автобус', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer('Такой стороны нет(')