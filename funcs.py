import imports
class Anti_Spam(imports.BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message : imports.Message):
        time_mes_last, chat_id = message.date.minute * 60 + message.date.second, message.chat.id
        if chat_id in imports.const.ANTI_SPAM_DICT:
            if time_mes_last - imports.const.ANTI_SPAM_DICT[chat_id] >= 2:
                imports.const.ANTI_SPAM_DICT[chat_id] = time_mes_last
                print('tru1', imports.const.ANTI_SPAM_DICT)
                return True
            else:
                print('fals', imports.const.ANTI_SPAM_DICT)
                return False
        else:
            imports.const.ANTI_SPAM_DICT[chat_id] = time_mes_last
            print('tru2', imports.const.ANTI_SPAM_DICT)
            return True
    
    

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