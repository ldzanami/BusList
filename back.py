from FSMClass import FSMChoiceBus
import funcs

async def back(message, state, USER_DATA, ras, ADMINS, ads):
    if await state.get_state() == FSMChoiceBus.choice_station:
        user = USER_DATA[message.from_user.id]
        rass = ras
        USER_DATA[message.from_user.id]['city'] = None
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 3, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(len(rass) + 3, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_city)
        # print(USER_DATA)

    elif await state.get_state() == FSMChoiceBus.choice_side:
        user = USER_DATA[message.from_user.id]
        rass = ras[user['city']]
        USER_DATA[message.from_user.id]['station'] = None
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_station)
        # print(USER_DATA)

    elif await state.get_state() == FSMChoiceBus.choice_bus:
        user = USER_DATA[message.from_user.id]
        rass = ras[user["city"]][user['station']]
        USER_DATA[message.from_user.id]['side'] = None
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_side)
        # print(USER_DATA)
    
    elif await state.get_state() == FSMChoiceBus.in_bus:
        user = USER_DATA[message.from_user.id]
        rass = ras[user["city"]][user['station']][user['side']]
        USER_DATA[message.from_user.id]['bus'] = None
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_bus)