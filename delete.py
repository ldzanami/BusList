from FSMClass import FSMChoiceBus
import funcs

async def delete(message, state, USER_DATA, ras, ADMINS, ads, MY_ID, bot):
    what = None
    user = USER_DATA[message.from_user.id]
    if await state.get_state() == FSMChoiceBus.delete_city:
        if message.text in ras:
            what = 'город'
            ras.pop(message.text)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(ras.keys()) + 3, sorted(ras.keys()) + ['/Добавить', '/Удалить', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(ras.keys()) + 3, sorted(ras.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такого города в списке нет(')
        await state.set_state(FSMChoiceBus.choice_city)

    elif await state.get_state() == FSMChoiceBus.delete_station:
        rass = ras[user['city']]
        if message.text in rass:
            what = f'{user["city"]} остановку'
            ras[user['city']].pop(message.text)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такой остановки в списке нет(')
        await state.set_state(FSMChoiceBus.choice_station)

    elif await state.get_state() == FSMChoiceBus.delete_side:
        rass = ras[user["city"]][user['station']]
        if message.text in rass:
            what = f'{user["city"]} {user["station"]} сторону'
            ras[user['city']][user['station']].pop(message.text)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такой стороны в списке нет(')
        await state.set_state(FSMChoiceBus.choice_side)

    elif await state.get_state() == FSMChoiceBus.delete_bus:
        rass = ras[user['city']][user['station']][user['side']]
        if message.text in rass:
            what = f'{user["city"]} {user["station"]} {user["side"]} автобус'
            ras[user['city']][user['station']][user['side']].pop(message.text)
            if message.from_user.id in ADMINS:
                keyboard = await funcs.create_Replykeyboard(len(ads) + len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
            else: keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такого автобуса в списке нет(')
        await state.set_state(FSMChoiceBus.choice_bus)

    elif await state.get_state() == FSMChoiceBus.delete_in_bus:
        hour = message.text.strip().split(':')
        if len(hour) == 2 and len(hour[0]) == 2 and len(hour[1]) == 2 and hour[0].isalnum() and hour[1].isalnum() and 0 <= int(hour[0]) <= 23 and 0 <= int(hour[1]) <= 59:
            hour = list(map(lambda x: str(int(x)), hour))
            rass = ras[user['city']][user['station']][user['side']][user['bus']]
            if hour[0] in rass:
                rass = ras[user['city']][user['station']][user['side']][user['bus']][hour[0]]
                if hour[1] in rass:
                    ras[user['city']][user['station']][user['side']][user['bus']][hour[0]].pop(hour[1])
                    if not rass:
                        ras[user['city']][user['station']][user['side']][user['bus']].pop(hour[0])
                    what = f'{user["city"]} {user["station"]} {user["side"]} {user["bus"]} время'
                    await message.answer('Удалил')
                else: await message.answer("Такого времени в списке нет")
            else: await message.answer("Такого времени в списке нет")
            await state.set_state(FSMChoiceBus.in_bus)
        else:
            await state.set_state(FSMChoiceBus.in_bus)
            await message.answer("Такого времени в списке нет")
    await funcs.save_db(ras)
    await bot.send_message(MY_ID, f'Пользователь: {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.id} удалил {what} {message.text}')
