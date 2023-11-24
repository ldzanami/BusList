from FSMClass import FSMChoiceBus

async def delete_state(message, state):
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