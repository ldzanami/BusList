from FSMClass import FSMChoiceBus
import funcs

async def choice_bus(message, state, ras, USER_DATA, ADMINS, ads):
    user = USER_DATA[message.from_user.id]
    rass = ras[user["city"]][user['station']][user['side']]
    if message.text in rass:
        USER_DATA[message.from_user.id]['bus'] = message.text
        await state.set_state(FSMChoiceBus.in_bus)
        if message.from_user.id in ADMINS:
            keyboard = await funcs.create_Replykeyboard(len(ads) + 5, ['/Расписание', '/Добавить', '/Удалить', '/Назад', '/Выход'] + ads, inString=2)
        else: keyboard = await funcs.create_Replykeyboard(5, ['/Расписание', '/Добавить', '/Удалить', '/Назад', '/Выход'], inString=2)
        await message.answer('Нашёл', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else: await message.answer("Такого автобуса в списке нет(")