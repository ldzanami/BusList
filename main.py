import imports
import funcs

bot = imports.Bot(token=imports.const.BOT_TOKEN)
dp = imports.Dispatcher()

dp.message.register(funcs.start_command, imports.Command(commands=["start"]))
dp.message.register(funcs.cats_command, imports.Command(commands=["cats", "c"]))
dp.message.register(funcs.anime_command, imports.Command(commands=["anime", "a"]))
dp.message.register(funcs.any_message)

if __name__ == '__main__':
    dp.run_polling(bot)