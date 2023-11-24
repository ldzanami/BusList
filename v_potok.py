import funcs
from FSMClass import FSMChoiceBus

async def v_potok(message, state):
    keyboard = await funcs.create_Replykeyboard(4, ['/BAN', '/UNBAN', '/MESSAGE', '/Выход'], inString=3)
    await message.answer("Я АБСОЛЮТ, И ВИЖУ ВСЁ!", reply_markup=keyboard.as_markup(resize_keyboard=True))
    await state.set_state(FSMChoiceBus.V_POTOKE_ABSOLUTE)