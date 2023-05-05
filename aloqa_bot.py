import time
import os
import threading

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import Message
from dotenv import *
from library.parsing import aloqabank
from library.database import insert_or_ignore_user, insert_currency,\
    get_last_currency, get_all_users, del_block

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(TOKEN, threaded=True)


def trigger_update():
    while True:
        if current := aloqabank():
            history = get_last_currency()
            if tuple(current) != history:
                insert_currency(*current)
                for user in get_all_users():
                    try:
                        bot.send_message(user[0],
                                         f"🔥 ОБНОВЛЕНИЕ \n\nКурс ЦБ: {current[2]} "
                                         f"\nAloqabank Покупка: {current[0]} сум"
                                         f"\nAloqabank Продажа: {current[1]} сум")
                    except ApiTelegramException:
                        del_block(user[0])
                    except Exception as e:
                        print(e)

            print('Курс не изменился')
        time.sleep(60 * 10)


thread = threading.Thread(target=trigger_update)
thread.start()


@bot.message_handler(commands=['start', 'help', 'about'])
def command_start(message: Message):
    """Приветствие пользователя"""
    if message.text == '/start':
        user_id = message.from_user.id
        if insert_or_ignore_user(user_id):
            bot.send_message(user_id,
                             "Добро пожаловать в бот, при изменении курса доллара в банке Aloqabank, "
                             "бот сам будет присылать обновление")
            send_currency(user_id)
        else:
            send_currency(user_id)


def send_currency(user_id):
    """Отправка курса по команде старт"""
    if result := aloqabank():
        bot.send_message(user_id, f"Курс ЦБ: {result[2]} "
                                  f"\nAloqabank Покупка:  {result[0]} сум"
                                  f"\nAloqabank Продажа:  {result[1]} сум")
        insert_currency(*result)


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
