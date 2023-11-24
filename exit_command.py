import funcs
from FSMClass import FSMChoiceBus

async def exit_command(message, state, USER_DATA : dict):
    keyboard = await funcs.create_Replykeyboard(2, ['/start', '/help'], inString=2)
    if await state.get_state() == FSMChoiceBus.V_POTOKE_ABSOLUTE:
        await message.answer('Единственный, кто может победить меня - это я сам...', reply_markup=keyboard.as_markup(resize_keyboard=True))
    else:
        await message.answer('*Выход*', reply_markup=keyboard.as_markup(resize_keyboard=True))
    try:
        USER_DATA.pop(message.from_user.id)
    except KeyError:
        USER_DATA[message.from_user.id] = 1
        USER_DATA.pop(message.from_user.id)
    # print(USER_DATA)
    await state.clear()