import imports
import funcs
import BusClass
from FSMClass import FSMChoiceBus

bot = imports.Bot(token=imports.const.BOT_TOKEN)
dp = imports.Dispatcher()
ads = ['/ABSOLUTE']
ignore_inputs = ['/start', '/Добавить', '/Удалить', '/Выход', '/help', '/Расписание', '/Назад', '/BAN', '/UNBAN', '/MESSAGE'] + ads



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='Выход'), ~imports.StateFilter(imports.default_state))
async def exit(message : imports.Message, state : imports.FSMContext):
    await imports.exit_command(message, state, imports.const.USER_DATA)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='ABSOLUTE'), lambda x: x.from_user.id in imports.const.ADMINS)
async def potok(message : imports.Message, state : imports.FSMContext):
    await imports.v_potok(message, state)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='MESSAGE'), imports.StateFilter(FSMChoiceBus.V_POTOKE_ABSOLUTE))
async def say_state(message : imports.Message, state : imports.FSMContext):
    await message.answer("ДАВАЙ!")
    await state.set_state(FSMChoiceBus.MESSAGE)



@dp.message(lambda x: funcs.isbanned(x), lambda x: x or x.text and x.text not in ignore_inputs, imports.StateFilter(FSMChoiceBus.MESSAGE))
async def say(message : imports.Message, state : imports.FSMContext):
    for i in imports.const.users.keys():
        await message.send_copy(i)
    await message.answer("ГОТОВО")
    await state.set_state(FSMChoiceBus.V_POTOKE_ABSOLUTE)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='UNBAN'), imports.StateFilter(FSMChoiceBus.V_POTOKE_ABSOLUTE))
async def unban_state(message : imports.Message, state : imports.FSMContext):
    keyboard = await funcs.create_Replykeyboard(len(imports.const.users.keys()) + 1, list(imports.const.users.keys()) + ['/Выход'], inString=2)
    await message.answer("Невозможно полностью восстановить то, что когда-то было разбито.", reply_markup=keyboard.as_markup(resize_keyboard=True))
    await state.set_state(FSMChoiceBus.UNBAN)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.F.text.isdigit(), imports.StateFilter(FSMChoiceBus.UNBAN))
async def unb(message : imports.Message, state : imports.FSMContext):
    await imports.unban(message, state, imports.const.users)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='BAN'), imports.StateFilter(FSMChoiceBus.V_POTOKE_ABSOLUTE))
async def ban_state(message : imports.Message, state : imports.FSMContext):
    keyboard = await funcs.create_Replykeyboard(len(imports.const.users.keys()) + 1, list(imports.const.users.keys()) + ['/Выход'], inString=2)
    await message.answer("Вы посмели бросить мне вызов, поэтому просто заставить вас сидеть недостаточно. На колени!".upper(), reply_markup=keyboard.as_markup(resize_keyboard=True))
    await state.set_state(FSMChoiceBus.BAN)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.F.text.isdigit(), imports.StateFilter(FSMChoiceBus.BAN))
async def b(message : imports.Message, state : imports.FSMContext):
    await imports.ban(message, state, imports.const.users, imports.const.MY_ID, imports.default_state, imports.const.ADMINS)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='help'))
async def help_command(message : imports.Message, state : imports.FSMContext):
    await message.answer(imports.const.help_message)



@dp.message(lambda x: funcs.isbanned(x), imports.CommandStart(), imports.StateFilter(imports.default_state, FSMChoiceBus.V_POTOKE_ABSOLUTE))
async def start(message : imports.Message, state : imports.FSMContext):
    await imports.start_command(message, state, imports.const.ADMINS, imports.const.USER_DATA, imports.const.ras, imports.const.users, ads)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='Расписание'), imports.StateFilter(FSMChoiceBus.in_bus))
async def printr(message : imports.Message, state : imports.FSMContext):
    await imports.print_ras(message, state, imports.const.ras, imports.const.USER_DATA)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='Добавить'), ~imports.StateFilter(imports.default_state))
async def addst(message : imports.Message, state : imports.FSMContext):
    await imports.add_state(message, state)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, lambda x: x.text not in ignore_inputs, imports.StateFilter(FSMChoiceBus.add_city, FSMChoiceBus.add_station, FSMChoiceBus.add_side, FSMChoiceBus.add_bus, FSMChoiceBus.add_in_bus))
async def a(message : imports.Message, state : imports.FSMContext):
    await imports.add(message, state, imports.const.USER_DATA, imports.const.ras, imports.const.ADMINS, ads, imports.const.MY_ID, bot)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='Назад'), ~imports.StateFilter(imports.default_state, FSMChoiceBus.choice_city))
async def bck(message : imports.Message, state : imports.FSMContext):
    await imports.back(message, state, imports.const.USER_DATA, imports.const.ras, imports.const.ADMINS, ads)



@dp.message(lambda x: funcs.isbanned(x), lambda x: x.from_user.id in imports.const.ADMINS, imports.Command(commands="Удалить"), ~imports.StateFilter(imports.default_state, FSMChoiceBus.add_city, FSMChoiceBus.add_station, FSMChoiceBus.add_side, FSMChoiceBus.add_bus, FSMChoiceBus.add_in_bus))
async def del_state(message : imports.Message, state : imports.FSMContext):
    await imports.delete_state(message, state)



@dp.message(lambda x: funcs.isbanned(x), imports.Command(commands='Удалить'), ~imports.StateFilter(imports.default_state, FSMChoiceBus.add_city, FSMChoiceBus.add_station, FSMChoiceBus.add_side, FSMChoiceBus.add_bus, FSMChoiceBus.add_in_bus))
async def delete_wrong(message : imports.Message, state : imports.FSMContext):
    await message.answer("У вас недостаточно прав для этого(")



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.StateFilter(FSMChoiceBus.delete_city, FSMChoiceBus.delete_station, FSMChoiceBus.delete_side, FSMChoiceBus.delete_bus, FSMChoiceBus.delete_in_bus))
async def delet(message : imports.Message, state : imports.FSMContext):
    await imports.delete(message, state, imports.const.USER_DATA, imports.const.ras, imports.const.ADMINS, ads, imports.const.MY_ID, bot)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.StateFilter(FSMChoiceBus.choice_city))
async def ch_city(message : imports.Message, state : imports.FSMContext):
    await imports.choice_city(message, state, imports.const.ras, imports.const.USER_DATA, imports.const.ADMINS, ads)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.StateFilter(FSMChoiceBus.choice_station))
async def ch_station(message : imports.Message, state : imports.FSMContext):
    await imports.choice_station(message, state, imports.const.ras, imports.const.USER_DATA, imports.const.ADMINS, ads)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.StateFilter(FSMChoiceBus.choice_side))
async def ch_side(message : imports.Message, state : imports.FSMContext):
    await imports.choice_side(message, state, imports.const.ras, imports.const.USER_DATA, imports.const.ADMINS, ads)



@dp.message(lambda x: funcs.isbanned(x), imports.F.text, imports.StateFilter(FSMChoiceBus.choice_bus))
async def ch_bus(message : imports.Message, state : imports.FSMContext):
    await imports.choice_bus(message, state, imports.const.ras, imports.const.USER_DATA, imports.const.ADMINS, ads)



@dp.message(lambda x: funcs.isbanned(x))
async def any(message : imports.Message, state : imports.FSMContext):
    pass



@dp.message(lambda x: not funcs.isbanned(x))
async def ban_message(message : imports.Message, state : imports.FSMContext):
    await message.answer("🚫ВАС ЗАБАНИЛИ🚫")



if __name__ == "__main__":
    dp.run_polling(bot)
