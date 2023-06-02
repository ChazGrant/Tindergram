from typing import DefaultDict

import telebot
from mysql.connector import Error, connect

from refactor.bot_functions import (bot_functions, init_bot, init_db,
                                    show_incoming_likes, show_main_menu,
                                    show_mutual_likes, show_outcoming_likes,
                                    show_profile, show_questionnaires, get_name)
from refactor.Database import Database
from User import User


with open("TOKEN.txt") as token_file:
    TOKEN = token_file.readline()
bot = telebot.TeleBot(TOKEN)
init_bot(TOKEN)
db_conn = init_db()
# user_id : user_info(e.g id, photo, description)
tmp_user_info = DefaultDict[int, User]

current_qu = None


@bot.message_handler(commands=["start"])
def initialize(message):
    """
        В БД поочерёдно заносятся поля для записи
        Если пользователь доходит до последнего шага то 
        все это comit'тится и пользователь появляется в БД
    """
    if db_conn.user_is_initialized(message.from_user.id):
        return

    tmp_user_info[message.from_user.id] = []
    with connect(
        host="localhost",
        user="mezzano",
        password="23561423",
        database="Tindergram"
    ) as connection:
        cursor = connection.cursor()
        user_ID = message.from_user.id
        # Добавляем юзера в БД
        query = ("INSERT INTO InitializedUsers (UserID) VALUES (%s)")
        data = (int(user_ID), )
        cursor.execute(query, data)

        connection.commit()

        bot.send_message(message.chat.id, "Для начала давайте создадим анкету.\nКак мне вас называть?")
        bot.register_next_step_handler(message, tmp_user_info, get_name)


while True:
    user_input = input()
    if user_input.lower() == "exit":
        break
    if user_input.lower() in bot_functions.keys():
        args = 15
        bot_functions[user_input.lower()](args)
    else:
        print("Unknown command")

# bot.infinity_polling()
# @bot.message_handler(commands=["start"])
