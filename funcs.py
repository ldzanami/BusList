import imports

async def create_Replykeyboard(how_much : int, texts : list[str], inString=1) -> imports.ReplyKeyboardBuilder:
    builder = imports.ReplyKeyboardBuilder()
    for i in range(how_much):
        builder.add(imports.KeyboardButton(text=texts[i]))
    builder.adjust(inString)
    return builder

async def create_Inlinekeyboard(how_much : int, texts : list[str], inString=1, CallbackData=None) -> imports.InlineKeyboardBuilder:
    builder = imports.InlineKeyboardBuilder()
    for i in range(how_much):
        builder.button(text=texts[i], callback_data=CallbackData)
    builder.adjust(inString)
    return builder

async def save_db(ras : dict):
    with open("db.json", "w", encoding="utf-8") as db:
        imports.json.dump(ras, db)

async def save_users(users : dict):
    with open("dbUsers.json", "w", encoding="utf-8") as dbUsers:
        imports.json.dump(users, dbUsers)

def isbanned(message : imports.Message):
    if str(message.from_user.id) in imports.const.users:
        return imports.const.users[str(message.from_user.id)][0]
    else: return True