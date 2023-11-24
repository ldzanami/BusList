import funcs
from FSMClass import FSMChoiceBus

async def unban(message, state, users):
    keyboard = await funcs.create_Replykeyboard(4, ['/BAN', '/UNBAN', '/MESSAGE', '/Выход'], inString=3)
    users[message.text][0] = 1
    await message.answer("ЧЕЛОВЕЧНОСТЬ ВОССТАНОВЛЕНА", reply_markup=keyboard.as_markup(resize_keyboard=True))
    await state.set_state(FSMChoiceBus.V_POTOKE_ABSOLUTE)
    await funcs.save_users(users)