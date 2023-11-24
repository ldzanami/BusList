import funcs
from FSMClass import FSMChoiceBus

async def add(message, state, USER_DATA, ras, ADMINS, ads, MY_ID, bot):
    what = None
    user = USER_DATA[message.from_user.id]
    if await state.get_state() == FSMChoiceBus.add_city:
        if len(message.text) <= 120:
            what = 'город'
            ras[message.text.strip('\'\|\/-\+\=\\><#@!$%^& ')] = ras.get(message.text, dict())
            await state.set_state(FSMChoiceBus.choice_city)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(ras.keys()) + 3, sorted(ras.keys()) + ['/Добавить', '/Удалить', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(ras.keys()) + 3, sorted(ras.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
            await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: 
            await state.set_state(FSMChoiceBus.choice_city)
            await message.answer('Длина названия должна быть не больше 120 символов')

    elif await state.get_state() == FSMChoiceBus.add_station:
        if len(message.text) <= 120:
            what = f'{user["city"]} остановку'
            rass = ras[user['city']]
            ras[user['city']][message.text.strip('\'\|\/-\+\=\\><#@!$%^& ')] = ras[user['city']].get(message.text, dict())
            await state.set_state(FSMChoiceBus.choice_station)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: 
            await state.set_state(FSMChoiceBus.choice_station)
            await message.answer('Длина названия должна быть не больше 120 символов')

    elif await state.get_state() == FSMChoiceBus.add_side:
        if len(message.text) <= 120:
            if message.text.strip().capitalize() in ['Левая', 'Правая']:
                what = f'{user["city"]} {user["station"]} сторону'
                rass = ras[user["city"]][user['station']]
                ras[user['city']][user['station']][message.text.strip('\'\|\/-\+\=\\><#@!$%^& ').capitalize()] = ras[user['city']][user['station']].get(message.text, dict())
                await state.set_state(FSMChoiceBus.choice_side)
                if message.from_user.id in ADMINS:
                    keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
                else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
                await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))
            else: 
                await state.set_state(FSMChoiceBus.choice_side)
                await message.answer('Такой стороны не бывает(')
        else: 
            await state.set_state(FSMChoiceBus.choice_side)
            await message.answer('Длина названия должна быть не больше 120 символов')

    elif await state.get_state() == FSMChoiceBus.add_bus:
        if len(message.text) <= 120:
            what = f'{user["city"]} {user["station"]} {user["side"]} автобус'
            rass = ras[user['city']][user['station']][user['side']]
            ras[user['city']][user['station']][user['side']][message.text.strip('\'\|\/-\+\=\\><#@!$%^& ')] = ras[user['city']][user['station']][user['side']].get(message.text, dict())
            await state.set_state(FSMChoiceBus.choice_bus)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: 
            await state.set_state(FSMChoiceBus.choice_bus)
            await message.answer('Длина названия должна быть не больше 120 символов')

    elif await state.get_state() == FSMChoiceBus.add_in_bus:
        hour = message.text.strip().split(':')
        if len(hour) == 2 and len(hour[0]) == 2 and len(hour[1]) == 2 and hour[0].isalnum() and hour[1].isalnum() and 0 <= int(hour[0]) <= 23 and 0 <= int(hour[1]) <= 59:
            hour = list(map(lambda x: str(int(x)), hour))
            rass = ras[user['city']][user['station']][user['side']][user['bus']]
            ras[user['city']][user['station']][user['side']][user['bus']][hour[0]] = ras[user['city']][user['station']][user['side']][user['bus']].get(hour[0], dict())
            if hour[1] not in ras[user['city']][user['station']][user['side']][user['bus']][hour[0]]:
                ras[user['city']][user['station']][user['side']][user['bus']][hour[0]][hour[1]] = []
            await message.answer('Добавил')
            what = f'{user["city"]} {user["station"]} {user["side"]} {user["bus"]} время'
            await state.set_state(FSMChoiceBus.in_bus)
        else:
            await state.set_state(FSMChoiceBus.in_bus)
            await message.answer("Введено неверное время")
    await funcs.save_db(ras)
    await bot.send_message(MY_ID, f'Пользователь: {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.id} добавил {what} {message.text}')
