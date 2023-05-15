# import telebot
from mysql.connector import connect, Error
# from keyboards import *
from bot_functions import (bot_functions, show_outcoming_likes, show_incoming_likes, 
    show_main_menu, show_mutual_likes, show_profile, show_questionnaires)

# bot = telebot.TeleBot("5391782983:AAFHwhF00_zk8RWNRGLBLToyE863S-qhUAo")

# user_id : user_info(e.g id, photo, description)
tmp_user_info = dict()

current_qu = None

@bot.message_handler(commands=['start'])
def initialize(message):
    '''
        В БД поочерёдно заносятся поля для записи
        Если пользователь доходит до последнего шага то 
        все это comit'тится и пользователь появляется в БД
    '''
    if user_is_initialized(message.from_user.id):
        return


    tmp_user_info[message.from_user.id] = []
    with connect(
        host="localhost",
        user="mezzano",
        password="23561423",
        database='Tindergram'
    ) as connection:
        cursor = connection.cursor()
        user_ID = message.from_user.id
        # Добавляем юзера в БД
        query = ("INSERT INTO InitializedUsers (UserID) VALUES (%s)")
        data = (int(user_ID), )
        cursor.execute(query, data)

        connection.commit()

        bot.send_message(message.chat.id, "Для начала давайте создадим анкету.\nКак мне вас называть?")
        bot.register_next_step_handler(message, get_name)

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
# @bot.message_handler(commands=['start'])
