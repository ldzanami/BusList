import imports
import funcs
import BusClass
from FSMClass import FSMChoiceBus

bot = imports.Bot(token=imports.const.BOT_TOKEN)
dp = imports.Dispatcher()

@dp.message(imports.CommandStart(), imports.StateFilter(imports.default_state))
async def start_command(message : imports.Message, state : imports.FSMContext):
    keyboard = await funcs.create_Replykeyboard(len(imports.const.ras.keys()) + 3, sorted(imports.const.ras.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
    await  message.answer("Бот для расписаний...", reply_markup=keyboard.as_markup(resize_keyboard=True))
    imports.const.USER_DATA[message.from_user.id] = {
        'city': None,
        'station': None,
        'side': None,
        'bus': None
    }
    # print(imports.const.USER_DATA)
    await state.set_state(FSMChoiceBus.choice_city)

@dp.message(imports.Command(commands='Расписание'), imports.StateFilter(FSMChoiceBus.in_bus))
async def print_ras(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    if imports.const.ras[user['city']][user['station']][user['side']][user['bus']]:
        bus = BusClass.Bus(imports.const.ras, user['city'], user['station'], user['side'], user['bus'], message)
        await bus.print_table()
        keyboard = await funcs.create_Inlinekeyboard(len(bus.list_commands) - 1, bus.list_commands[:len(bus.list_commands) - 1], CallbackData="adadadad")
        await message.answer(bus.list_commands[-1], reply_markup=keyboard.as_markup())
    else: await message.answer('Здесь пока пусто...')

@dp.message(imports.Command(commands='Добавить'), ~imports.StateFilter(imports.default_state))
async def add_state(message : imports.Message, state : imports.FSMContext):
    if await state.get_state() == FSMChoiceBus.choice_city:
        await state.set_state(FSMChoiceBus.add_city)
        await message.answer('Введите название города')

    elif await state.get_state() == FSMChoiceBus.choice_station:
        await state.set_state(FSMChoiceBus.add_station)
        await message.answer('Введите название остановки')

    elif await state.get_state() == FSMChoiceBus.choice_side:
        await state.set_state(FSMChoiceBus.add_side)
        await message.answer('Введите сторону (Левая/Правая)')

    elif await state.get_state() == FSMChoiceBus.choice_bus:
        await state.set_state(FSMChoiceBus.add_bus)
        await message.answer('Введите номер автобуса (Примеры: 32 Пл.Южная; 112С; 23)')
    
    elif await state.get_state() == FSMChoiceBus.in_bus:
        await state.set_state(FSMChoiceBus.add_in_bus)
        await message.answer('Введите время прибытия на остановку (Пример: 12:53)')

@dp.message(imports.F.text, imports.StateFilter(FSMChoiceBus.add_city, FSMChoiceBus.add_station, FSMChoiceBus.add_side, FSMChoiceBus.add_bus, FSMChoiceBus.add_in_bus))
async def add(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    if await state.get_state() == FSMChoiceBus.add_city:
        what = 'город'
        imports.const.ras[message.text.strip('\'\|",.\/:;`~-\+\=]\[{\}()]?><#@!$%^&* ')] = imports.const.ras.get(message.text, dict())
        await state.set_state(FSMChoiceBus.choice_city)
        keyboard = await funcs.create_Replykeyboard(len(imports.const.ras.keys()) + 3, sorted(imports.const.ras.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
        await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))

    elif await state.get_state() == FSMChoiceBus.add_station:
        what = f'{user["city"]} остановку'
        rass = imports.const.ras[user['city']]
        imports.const.ras[user['city']][message.text.strip('\'\|",.\/:;`~-\+\=]\[{\}()]?><#@!$%^&* ')] = imports.const.ras[user['city']].get(message.text, dict())
        await state.set_state(FSMChoiceBus.choice_station)
        keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))

    elif await state.get_state() == FSMChoiceBus.add_side:
        if message.text.strip().capitalize() in ['Левая', 'Правая']: 
            what = f'{user["city"]} {user["station"]} сторону'
            rass = imports.const.ras[user["city"]][user['station']]
            imports.const.ras[user['city']][user['station']][message.text.strip('\'\|",.\/:;`~-\+\=]\[{\}()]?><#@!$%^&* ').capitalize()] = imports.const.ras[user['city']][user['station']].get(message.text, dict())
            await state.set_state(FSMChoiceBus.choice_side)
            keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer("*WRONG INPUT*")

    elif await state.get_state() == FSMChoiceBus.add_bus:
        what = f'{user["city"]} {user["station"]} {user["side"]} автобус'
        rass = imports.const.ras[user['city']][user['station']][user['side']]
        imports.const.ras[user['city']][user['station']][user['side']][message.text.strip('\'\|",.\/:;`~-\+\=]\[{\}()]?><#@!$%^&* ')] = imports.const.ras[user['city']][user['station']][user['side']].get(message.text, dict())
        await state.set_state(FSMChoiceBus.choice_bus)
        keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Записал', reply_markup=keyboard.as_markup(resize_keyboard=True))

    elif await state.get_state() == FSMChoiceBus.add_in_bus:
        hour = message.text.strip().split(':')
        if len(hour) == 2 and len(hour[0]) == 2 and len(hour[1]) == 2 and hour[0].isalnum() and hour[1].isalnum() and 0 <= int(hour[0]) <= 23 and 0 <= int(hour[1]) <= 59:
            hour = list(map(lambda x: str(int(x)), hour))
            rass = imports.const.ras[user['city']][user['station']][user['side']][user['bus']]
            imports.const.ras[user['city']][user['station']][user['side']][user['bus']][hour[0]] = imports.const.ras[user['city']][user['station']][user['side']][user['bus']].get(hour[0], dict())
            if hour[1] not in imports.const.ras[user['city']][user['station']][user['side']][user['bus']][hour[0]]:
                imports.const.ras[user['city']][user['station']][user['side']][user['bus']][hour[0]][hour[1]] = []
            await message.answer('Добавил')
            what = f'{user["city"]} {user["station"]} {user["side"]} {user["bus"]} время'
            await state.set_state(FSMChoiceBus.in_bus)
        else:
            await state.set_state(FSMChoiceBus.in_bus)
            await message.answer("Введено неверное время")
    await funcs.save_db(imports.const.ras)
    await bot.send_message(imports.const.MY_ID, f'Пользователь: {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.id} добавил {what} {message.text}')

@dp.message(imports.Command(commands='Выход'), ~imports.StateFilter(imports.default_state))
async def exit_command(message : imports.Message, state : imports.FSMContext):
    keyboard = await funcs.create_Replykeyboard(1, ['/start'], inString=1)
    await message.answer('*Выход*', reply_markup=keyboard.as_markup(resize_keyboard=True))
    imports.const.USER_DATA.pop(message.from_user.id)
    # print(imports.const.USER_DATA)
    await state.clear()

@dp.message(imports.Command(commands='Назад'), ~imports.StateFilter(imports.default_state, FSMChoiceBus.choice_city))
async def back(message : imports.Message, state : imports.FSMContext):
    if await state.get_state() == FSMChoiceBus.choice_station:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras
        imports.const.USER_DATA[message.from_user.id]['city'] = None
        keyboard = await funcs.create_Replykeyboard(len(rass) + 3, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_city)
        # print(imports.const.USER_DATA)

    elif await state.get_state() == FSMChoiceBus.choice_side:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras[user['city']]
        imports.const.USER_DATA[message.from_user.id]['station'] = None
        keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_station)
        # print(imports.const.USER_DATA)

    elif await state.get_state() == FSMChoiceBus.choice_bus:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras[user["city"]][user['station']]
        imports.const.USER_DATA[message.from_user.id]['side'] = None
        keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_side)
        # print(imports.const.USER_DATA)
    
    elif await state.get_state() == FSMChoiceBus.in_bus:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras[user["city"]][user['station']][user['side']]
        imports.const.USER_DATA[message.from_user.id]['bus'] = None
        keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("*Назад*", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_bus)

@dp.message(lambda x: x.from_user.id in imports.const.ADMINS, imports.Command(commands="Удалить"), ~imports.StateFilter(imports.default_state, FSMChoiceBus.add_city, FSMChoiceBus.add_station, FSMChoiceBus.add_side, FSMChoiceBus.add_bus, FSMChoiceBus.add_in_bus))
async def delete_state(message : imports.Message, state : imports.FSMContext):
    if await state.get_state() == FSMChoiceBus.choice_city:
        await state.set_state(FSMChoiceBus.delete_city)
        await message.answer('Выберите из списка элемент, который хотите удалить')

    elif await state.get_state() == FSMChoiceBus.choice_station:
        await state.set_state(FSMChoiceBus.delete_station)
        await message.answer('Выберите из списка элемент, который хотите удалить')

    elif await state.get_state() == FSMChoiceBus.choice_side:
        await state.set_state(FSMChoiceBus.delete_side)
        await message.answer('Выберите из списка элемент, который хотите удалить')

    elif await state.get_state() == FSMChoiceBus.choice_bus:
        await state.set_state(FSMChoiceBus.delete_bus)
        await message.answer('Выберите из списка элемент, который хотите удалить')
    
    elif await state.get_state() == FSMChoiceBus.in_bus:
        await state.set_state(FSMChoiceBus.delete_in_bus)
        await message.answer('Впишите время, которое хотите удалить')

@dp.message(imports.Command(commands='Удалить'), ~imports.StateFilter(imports.default_state, FSMChoiceBus.add_city, FSMChoiceBus.add_station, FSMChoiceBus.add_side, FSMChoiceBus.add_bus, FSMChoiceBus.add_in_bus))
async def delete_wrong(message : imports.Message):
    await message.answer("У вас недостаточно прав для этого(")

@dp.message(imports.F.text, imports.StateFilter(FSMChoiceBus.delete_city, FSMChoiceBus.delete_station, FSMChoiceBus.delete_side, FSMChoiceBus.delete_bus, FSMChoiceBus.delete_in_bus))
async def delete(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    if await state.get_state() == FSMChoiceBus.delete_city:
        if message.text in imports.const.ras:
            what = 'город'
            imports.const.ras.pop(message.text)
            keyboard = await funcs.create_Replykeyboard(len(imports.const.ras.keys()) + 3, sorted(imports.const.ras.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такого города в списке нет(')
        await state.set_state(FSMChoiceBus.choice_city)

    elif await state.get_state() == FSMChoiceBus.delete_station:
        rass = imports.const.ras[user['city']]
        if message.text in rass:
            what = f'{user["city"]} остановку'
            imports.const.ras[user['city']].pop(message.text)
            keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такой остановки в списке нет(')
        await state.set_state(FSMChoiceBus.choice_station)

    elif await state.get_state() == FSMChoiceBus.delete_side:
        rass = imports.const.ras[user["city"]][user['station']]
        if message.text in rass:
            what = f'{user["city"]} {user["station"]} сторону'
            imports.const.ras[user['city']][user['station']].pop(message.text)
            keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такой стороны в списке нет(')
        await state.set_state(FSMChoiceBus.choice_side)

    elif await state.get_state() == FSMChoiceBus.delete_bus:
        rass = imports.const.ras[user['city']][user['station']][user['side']]
        if message.text in rass:
            what = f'{user["city"]} {user["station"]} {user["side"]} автобус'
            imports.const.ras[user['city']][user['station']][user['side']].pop(message.text)
            keyboard = await funcs.create_Replykeyboard(len(rass) + 4, sorted(rass.keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
            await message.answer('Удалил', reply_markup=keyboard.as_markup(resize_keyboard=True))
        else: await message.answer('Такого автобуса в списке нет(')
        await state.set_state(FSMChoiceBus.choice_bus)

    elif await state.get_state() == FSMChoiceBus.delete_in_bus:
        hour = message.text.strip().split(':')
        if len(hour) == 2 and len(hour[0]) == 2 and len(hour[1]) == 2 and hour[0].isalnum() and hour[1].isalnum() and 0 <= int(hour[0]) <= 23 and 0 <= int(hour[1]) <= 59:
            hour = list(map(lambda x: str(int(x)), hour))
            rass = imports.const.ras[user['city']][user['station']][user['side']][user['bus']]
            if hour[0] in rass:
                rass = imports.const.ras[user['city']][user['station']][user['side']][user['bus']][hour[0]]
                if hour[1] in rass:
                    imports.const.ras[user['city']][user['station']][user['side']][user['bus']][hour[0]].pop(hour[1])
                    if not rass:
                        imports.const.ras[user['city']][user['station']][user['side']][user['bus']].pop(hour[0])
                    what = f'{user["city"]} {user["station"]} {user["side"]} {user["bus"]} время'
                    await message.answer('Удалил')
                else: await message.answer("Такого времени в списке нет")
            else: await message.answer("Такого времени в списке нет")
            await state.set_state(FSMChoiceBus.in_bus)
        else:
            await state.set_state(FSMChoiceBus.in_bus)
            await message.answer("Такого времени в списке нет")
    await funcs.save_db(imports.const.ras)
    await bot.send_message(imports.const.MY_ID, f'Пользователь: {message.from_user.username} {message.from_user.first_name} {message.from_user.last_name} {message.from_user.id} удалил {what} {message.text}')

@dp.message(imports.F.text, imports.StateFilter(FSMChoiceBus.choice_city))
async def choice_bus(message : imports.Message, state : imports.FSMContext):
    rass = imports.const.ras
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]["city"] = message.text
        # print(imports.const.USER_DATA)
        await state.set_state(FSMChoiceBus.choice_station)
        keyboard = await funcs.create_Replykeyboard(len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer("OK", reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer("Такого города в списке нет(")

@dp.message(imports.F.text, imports.StateFilter(FSMChoiceBus.choice_station))
async def choice_station(message : imports.Message, state : imports.FSMContext):
    rass = imports.const.ras[imports.const.USER_DATA[message.from_user.id]['city']]
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]['station'] = message.text
        # print(imports.const.USER_DATA)
        await state.set_state(FSMChoiceBus.choice_side)
        keyboard = await funcs.create_Replykeyboard(len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Хорошо', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer("Такой остановки в списке нет(")

@dp.message(imports.F.text, imports.StateFilter(FSMChoiceBus.choice_side))
async def choice_side(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    rass = imports.const.ras[user["city"]][user['station']]
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]['side'] = message.text
        # print(imports.const.USER_DATA)
        await state.set_state(FSMChoiceBus.choice_bus)
        keyboard = await funcs.create_Replykeyboard(len(rass[message.text]) + 4, sorted(rass[message.text].keys()) + ['/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Посмотрим', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer('Такой стороны нет(')

@dp.message(imports.F.text, imports.StateFilter(FSMChoiceBus.choice_bus))
async def choice_bus(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    rass = imports.const.ras[user["city"]][user['station']][user['side']]
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]['bus'] = message.text
        await state.set_state(FSMChoiceBus.in_bus)
        keyboard = await funcs.create_Replykeyboard(5, ['/Расписание', '/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Нашёл', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer("Такого автобуса в списке нет(")

@dp.message()
async def any(message : imports.Message, state : imports.FSMContext):
    pass

if __name__ == "__main__":
    dp.run_polling(bot)