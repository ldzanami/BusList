from FSMClass import FSMChoiceBus
import funcs

async def choice_station(message, state, ras, USER_DATA, ADMINS, ads):
    rass = ras[USER_DATA[message.from_user.id]['city']]
    if message.text in rass:
        USER_DATA[message.from_user.id]['station'] = message.text
        # print(USER_DATA)
        await state.set_state(FSMChoiceBus.choice_side)
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Выберите сторону', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer("Такой остановки в списке нет(")