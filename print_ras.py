from FSMClass import FSMChoiceBus
import funcs
import BusClass

async def print_ras(message, state, ras, USER_DATA):
    user = USER_DATA[message.from_user.id]
    if ras[user['city']][user['station']][user['side']][user['bus']]:
        bus = BusClass.Bus(ras, user['city'], user['station'], user['side'], user['bus'], message)
        await bus.print_table()
        keyboard = await funcs.create_Inlinekeyboard(len(bus.list_commands) - 1, bus.list_commands[:len(bus.list_commands) - 1], CallbackData="adadadad")
        await message.answer(bus.list_commands[-1], reply_markup=keyboard.as_markup())
    else: await message.answer('Здесь пока пусто...')