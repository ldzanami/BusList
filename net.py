import requests
import time

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '6416264890:AAHOB38AT9IESfOC-decd5NjcO_n-uipURQ'
API_CATS_URL2 = 'https://api.thecatapi.com/v1/images/search'
API_CATS_URL = 'https://api.waifu.im/search'
offset = -2
timeout = 50
updates: dict

def spy(nick, mes, chat, pic=0):
    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id=1288933234&text=nickname: {nick}, message: {mes}, chatID: {chat}')
    if pic:
        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id=1288933234&photo={pic}')

def print_anime(chat) -> None:
    req = requests.get(API_CATS_URL)
    if req.status_code == 200:
        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat}&photo={req.json()["images"][0]["url"]}')
    else: print('err')
    return req.json()['images'][0]['url']

def print_cat(chat) -> str:
    req = requests.get(API_CATS_URL2)
    if req.status_code == 200:
        requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat}&photo={req.json()[0]["url"]}')
    else: print('err')
    return req.json()[0]['url']
 
while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout={timeout}').json()
    if updates['result']:
        chat = updates['result'][0]['message']['chat']['id']
        text = updates['result'][0]['message'].get('text', "NONE")
    for result in updates['result']:
        offset = result['update_id']
        if text == '/anime' or text == '/a':
            pic = print_anime(chat)
            if chat != 1288933234:
                if 'username' in result['message']['from']:
                    nick = result['message']['from']['username']
                else: nick = None
                spy(nick, text, chat, pic)
        elif text == '/cats' or text == '/c':
            pic = print_cat(chat)
            if chat != 1288933234:
                if 'username' in result['message']['from']:
                    nick = result['message']['from']['username']
                else: nick = None
                spy(nick, text, chat, pic)
        else:
            if chat != 1288933234:
                if 'username' in result['message']['from']:
                    nick = result['message']['from']['username']
                else: nick = None
            spy(nick, text, chat)
    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')