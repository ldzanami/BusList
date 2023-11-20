import imports
import funcs
import BusClass
from FSMClass import FSMChoiceBus

bot = imports.Bot(token=imports.const.BOT_TOKEN)
dp = imports.Dispatcher()

@dp.message(imports.CommandStart(), imports.StateFilter(imports.default_state))
async def start_command(message : imports.Message, state : imports.FSMContext):
    await  message.answer("Бот для расписаний...", reply_markup=funcs.create_Replykeyboard(len(imports.const.ras.keys()) + 1, sorted(imports.const.ras.keys()) + ["/Выход"], inString=2).as_markup(resize_keyboard=True))
    imports.const.USER_DATA[message.from_user.id] = {
        'city': None,
        'station': None,
        'side': None,
    }
    # print(imports.const.USER_DATA)
    await state.set_state(FSMChoiceBus.choice_city)

@dp.message(imports.Command(commands='Выход'), ~imports.StateFilter(imports.default_state))
async def exit_command(message : imports.Message, state : imports.FSMContext):
    await message.answer('*Выход*', reply_markup=funcs.create_Replykeyboard(1, ['/start'], inString=1).as_markup(resize_keyboard=True))
    imports.const.USER_DATA.pop(message.from_user.id)
    # print(imports.const.USER_DATA)
    await state.clear()

@dp.message(imports.Command(commands='Назад'), ~imports.StateFilter(imports.default_state, FSMChoiceBus.choice_city))
async def back(message : imports.Message, state : imports.FSMContext):
    if await state.get_state() == FSMChoiceBus.choice_station:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras
        imports.const.USER_DATA[message.from_user.id]['city'] = None
        await message.answer("*Назад*", reply_markup=funcs.create_Replykeyboard(len(rass) + 1, sorted(rass.keys()) + ['/Выход'], inString=2).as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_city)
        # print(imports.const.USER_DATA)

    
    elif await state.get_state() == FSMChoiceBus.choice_side:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras[user['city']]
        imports.const.USER_DATA[message.from_user.id]['station'] = None
        await message.answer("*Назад*", reply_markup=funcs.create_Replykeyboard(len(rass) + 2, sorted(rass.keys()) + ['/Назад', '/Выход'], inString=2).as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_station)
        # print(imports.const.USER_DATA)

    elif await state.get_state() == FSMChoiceBus.choice_bus:
        user = imports.const.USER_DATA[message.from_user.id]
        rass = imports.const.ras[user["city"]][user['station']]
        imports.const.USER_DATA[message.from_user.id]['side'] = None
        await message.answer("*Назад*", reply_markup=funcs.create_Replykeyboard(len(rass) + 2, sorted(rass.keys()) + ['/Назад', '/Выход'], inString=2).as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.choice_side)
        # print(imports.const.USER_DATA)

@dp.message(imports.StateFilter(FSMChoiceBus.choice_city))
async def choice_bus(message : imports.Message, state : imports.FSMContext):
    rass = imports.const.ras
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]["city"] = message.text
        # print(imports.const.USER_DATA)
        await state.set_state(FSMChoiceBus.choice_station)
        await message.answer("OK", reply_markup=funcs.create_Replykeyboard(len(rass[message.text]) + 2, sorted(rass[message.text].keys()) + ['/Назад', '/Выход'], inString=2).as_markup(resize_keyboard=True))
    else: await message.answer("Такого города в списке нет(")

@dp.message(imports.StateFilter(FSMChoiceBus.choice_station))
async def choice_station(message : imports.Message, state : imports.FSMContext):
    rass = imports.const.ras[imports.const.USER_DATA[message.from_user.id]['city']]
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]['station'] = message.text
        # print(imports.const.USER_DATA)
        await state.set_state(FSMChoiceBus.choice_side)
        await message.answer('Хорошо', reply_markup=funcs.create_Replykeyboard(len(rass[message.text]) + 2, sorted(rass[message.text].keys()) + ['/Назад', '/Выход'], inString=2).as_markup(resize_keyboard=True))
    else: await message.answer("Такой остановки в списке нет(")

@dp.message(imports.StateFilter(FSMChoiceBus.choice_side))
async def choice_side(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    rass = imports.const.ras[user["city"]][user['station']]
    if message.text in rass:
        imports.const.USER_DATA[message.from_user.id]['side'] = message.text
        # print(imports.const.USER_DATA)
        await state.set_state(FSMChoiceBus.choice_bus)
        await message.answer('Посмотрим', reply_markup=funcs.create_Replykeyboard(len(rass[message.text]) + 2, sorted(rass[message.text].keys()) + ['/Назад', '/Выход'], inString=2).as_markup(resize_keyboard=True))
    else: await message.answer('Такой стороны нет(')

@dp.message(imports.StateFilter(FSMChoiceBus.choice_bus))
async def choice_bus(message : imports.Message, state : imports.FSMContext):
    user = imports.const.USER_DATA[message.from_user.id]
    rass = imports.const.ras[user["city"]][user['station']][user['side']]
    if message.text in rass:
        bus = BusClass.Bus(imports.const.ras, user['city'], user['station'], user['side'], message.text)
        await bus.print_table()
        await message.answer(bus.list_commands[-1], reply_markup=funcs.create_Inlinekeyboard(len(bus.list_commands) - 1, bus.list_commands[:len(bus.list_commands) - 1], inString=2, CallbackData="adadadad").as_markup())
    else: await message.answer("Такого автобуса в списке нет(")



@dp.message()
async def any(message : imports.Message, state : imports.FSMContext):
    pass

if __name__ == "__main__":
    dp.run_polling(bot)