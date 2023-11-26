from FSMClass import FSMChoiceBus
import funcs

async def ban(message, state, users, MY_ID, default_state, ADMINS):
    if str(message.from_user.id) == message.text or message.text in list(map(str, ADMINS)) and message.from_user.id != MY_ID:
        await message.answer('Это френдли фаер - огонь по своим...')
        return
    if str(MY_ID) == message.text:
        users[str(message.from_user.id)][0] = 0
        await message.answer("ГЛУПЕЦ, ВОЗОМНИВШИЙ СЕБЯ БОГОМ, ЕДИНСТВЕННЫЙ, КТО МОЖЕТ ПОБЕДИТЬ МЕНЯ - ЭТО Я САМ!!!")
        await state.set_state(default_state)
    else:
        keyboard = await funcs.create_Replykeyboard(4, ['/BAN', '/UNBAN', '/MESSAGE', '/Выход'], inString=3)
        users[message.text][0] = 0
        await message.answer("В падении нет ничего постыдного. По-настоящему стыдно не подняться после падения.", reply_markup=keyboard.as_markup(resize_keyboard=True))
        await state.set_state(FSMChoiceBus.V_POTOKE_ABSOLUTE)
    await funcs.save_users(users)