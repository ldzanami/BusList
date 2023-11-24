from FSMClass import FSMChoiceBus

async def add_state(message, state):
    if await state.get_state() == FSMChoiceBus.choice_city:
        await state.set_state(FSMChoiceBus.add_city)
        await message.answer('Введите название города')

    elif await state.get_state() == FSMChoiceBus.choice_station:
        await state.set_state(FSMChoiceBus.add_station)
        await message.answer('Введите название остановки')

    elif await state.get_state() == FSMChoiceBus.choice_side:
        await state.set_state(FSMChoiceBus.add_side)
        await message.answer('Введите сторону (Левая/Правая)')

    elif await state.get_state() == FSMChoiceBus.choice_bus:
        await state.set_state(FSMChoiceBus.add_bus)
        await message.answer('Введите номер автобуса (Примеры: 32 Пл.Южная; 112С; 23)')
    
    elif await state.get_state() == FSMChoiceBus.in_bus:
        await state.set_state(FSMChoiceBus.add_in_bus)
        await message.answer('Введите время прибытия на остановку (Пример: 12:53)')