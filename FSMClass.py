import imports

class FSMChoiceBus(imports.StatesGroup):
    choice_city = imports.State()
    choice_station = imports.State()
    choice_side = imports.State()
    choice_bus = imports.State()
    V_POTOKE_ABSOLUTE = imports.State()
