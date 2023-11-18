import imports

kb = [
    [
        imports.KeyboardButton(text='/a'),
        imports.KeyboardButton(text='/c')
     ]
]
keyboard = imports.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)