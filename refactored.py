import telebot
from mysql.connector import connect, Error
from keyboards import *
from bot_functions import *

bot = telebot.TeleBot("5391782983:AAFHwhF00_zk8RWNRGLBLToyE863S-qhUAo")

# user_id : user_info(e.g id, photo, description)
tmp_user_info = dict()

current_qu = None

bot.infinity_polling()