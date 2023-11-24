from FSMClass import FSMChoiceBus
import funcs

async def start_command(message, state, ADMINS, USER_DATA, ras, users, ads):
    if message.from_user.id in ADMINS:
        keyboard = await funcs.create_Replykeyboard(len(ads) + len(ras.keys()) + 3, sorted(ras.keys()) + ['/Добавить', '/Удалить', '/Выход'] + ads, inString=2)
    else: keyboard = await funcs.create_Replykeyboard(len(ras.keys()) + 3, sorted(ras.keys()) + ['/Добавить', '/Удалить', '/Выход'], inString=2)
    await  message.answer("Выберите город", reply_markup=keyboard.as_markup(resize_keyboard=True))
    USER_DATA[message.from_user.id] = {
        'city': None,
        'station': None,
        'side': None,
        'bus': None
    }
    # print(USER_DATA)
    await state.set_state(FSMChoiceBus.choice_city)
    users[str(message.from_user.id)] = users.get(str(message.from_user.id), [1, message.from_user.full_name, message.from_user.username])
    await funcs.save_users(users)