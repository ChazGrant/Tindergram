import telebot
from telebot import types
import random
import randomname
from questionnaire import Questionnaire
from mysql.connector import connect, Error

TOKEN = open("TOKEN.txt").readline()
bot = telebot.TeleBot(TOKEN)

tmp_user_info = dict()

current_qu = None

'''
    t.me/{message.chat.username} - ссылка в ЛС
    bot.send_message(message.chat.id, text=f"<a href='{current_qu.user_link}'>{current_qu.name}</a>", parse_mode="HTML")
'''

users_pressed_start = list()

def makeSomeRandomQuestionnaires():
    for i in range(7):
        age = random.randrange(18, 45)
        name = randomname.get_name()
        desc = f"Я рандомная анкета №{i}"
        photo = open("ph.jpg", "rb")
        users["905463602"] = Questionnaire(photo, name, age, desc, "t.me/xavlegbmaofffassssitimi")

questionnaire_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Лайк')
itembtn2 = types.KeyboardButton('Скип')
itembtn3 = types.KeyboardButton('Главное меню')
questionnaire_keyboard.add(itembtn1, itembtn2, itembtn3)

main_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Анкеты')
itembtn2 = types.KeyboardButton('Профиль')
itembtn3 = types.KeyboardButton('Помощь')
itembtn4 = types.KeyboardButton('Взаимные лайки')
itembtn5 = types.KeyboardButton('Входящие лайки')
itembtn6 = types.KeyboardButton('Исходящие лайки')
main_keyboard.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

### Likes Switcher ###

next_keyboard = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('Следующая')
itembtn2 = types.KeyboardButton('Выход')
next_keyboard.add(itembtn1, itembtn2)

prev_keyboard = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('Предыдущая')
itembtn2 = types.KeyboardButton('Выход')
prev_keyboard.add(itembtn1, itembtn2)

next_prev_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Предыдущая')
itembtn2 = types.KeyboardButton('Следующая')
itembtn3 = types.KeyboardButton('Выход')
next_prev_keyboard.add(itembtn1, itembtn2, itembtn3)

exit_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Выход')
exit_keyboard.add(itembtn1)

### ### ### ### ### ### ### ### ### ###

like_skip_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Лайк')
itembtn2 = types.KeyboardButton('Пропустить')
itembtn3 = types.KeyboardButton('Выход')
like_skip_keyboard.add(itembtn1, itembtn2, itembtn3)

profile_keybaord = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Удалить анкету')
itembtn2 = types.KeyboardButton('Изменить анкету')
itembtn3 = types.KeyboardButton('Главное меню')
profile_keybaord.add(itembtn1, itembtn2, itembtn3)

yes_no_keyboard = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Да')
itembtn2 = types.KeyboardButton('Нет')
yes_no_keyboard.add(itembtn1, itembtn2)

def format_questionnaire(user_info):
    text = f"{user_info[0]} {user_info[1]}, {user_info[2]}\n{user_info[3]}"
    photo = user_info[6]

    return {
        "text" : text,
        "photo": photo,
        "user_id": user_info[5]
    }

def get_profile_info(user_id):
    try:
        with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT Name, Age, City, Description, UserLink, UserID, Photo FROM Questionnaires WHERE UserID = {int(user_id)}")
            user_info = cursor.fetchone()

            result = format_questionnaire(user_info)

            return result
    except Exception as e:
        print(e)

def insert_questionnaire(message, credentials):
    try:
        print("Credentials" + str(credentials) + "\n\n\n")
        with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            user_link = get_user_link(message.from_user.username)
            cursor = connection.cursor()
            
            query = "INSERT INTO Questionnaires (UserID, Name, Age, City, Description, Photo, UserLink) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            vals = (int(message.from_user.id), credentials[0], credentials[1], credentials[2], credentials[3], credentials[4], user_link)

            cursor.execute(query, vals)

            connection.commit()
            return True
    except Error as e:
        print(e)
        return False

def get_all_questionnaires(current_user_id):
    with connect(
        host="localhost",
        user="mezzano",
        password="23561423",
        database='Tindergram'
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT Name, Age, City, Description, UserLink, UserID, Photo FROM Questionnaires WHERE UserID <> {int(current_user_id)}")
        records = cursor.fetchall()

        return records

def get_random_questionnaire(current_user_id):
    all_questionnaires = get_all_questionnaires(current_user_id)
    # Если анкет нет
    if not all_questionnaires:
        return dict()
    user_info = random.choice(all_questionnaires)

    profile_info = format_questionnaire(user_info)

    return profile_info

def user_is_initialized(user_id):
    with connect(
        host="localhost",
        user="mezzano",
        password="23561423",
        database='Tindergram'
    ) as connection:
        cursor = connection.cursor()
        # Проверяем есть ли юзер в бд
        cursor.execute("SELECT * FROM Questionnaires")
        all_ids = cursor.fetchall()
        for cnt in range(len(all_ids)):
            all_ids[cnt] = all_ids[cnt][0]

        if all_ids == []:
            return False
        for user in all_ids:
            if int(user_id) == int(user):
                return True

    return False

def get_user_link(username):
    text = f"t.me/{username}'"

    return text

def get_user_with_link(user_id):
    try:
        with connect(
        host="localhost",
        user="mezzano",
        password="23561423",
        database='Tindergram'
        ) as connection:
            cursor = connection.cursor()

            cursor.execute(f"SELECT UserLink FROM Questionnaires WHERE UserID = {user_id}")
            user_link = cursor.fetchone()[0]

            return user_link

    except Exception as e:
        print(e)

        return 0

def messages_handler(messages):
    try:
        # print(messages)
        print("chat id ", messages[0].chat.id)
        print("user id ", messages[0].from_user.id)
        # print(messages[0].photo[0].file_id)
        #new_file = bot.get_file(messages[1].photo[-1].file_id)
        #downloaded_photo = bot.download_file(new_file.file_path)
        # print(new_file)
        # bot.send_photo(messages[0].chat.id, downloaded_photo, "Это ваше фото?)")
        # print(downloaded_photo)
    except Exception as e:
        print(e)

    for message in messages:
        if message.text == "/start" or user_is_initialized(messages[0].from_user.id):
            return

        bot.reply_to(messages[0], "Вы ещё не написали команду /start")

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

def get_name(message):
    if message.content_type == "text":
        tmp_user_info[message.from_user.id].append(message.text)
        bot.send_message(message.chat.id, "Сколько вам лет")
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.chat.id, "Вы должны отправить мне текст")
        bot.register_next_step_handler(message, get_name)

def get_age(message):
    if message.content_type == "text":
        # Check for int
        try:
            age = int(message.text)
            if age < 16:
                bot.send_message(message.chat.id, "Возраст должен быть больше 16")
                bot.register_next_step_handler(message, get_age)
                return

            tmp_user_info[message.from_user.id].append(age)
            bot.send_message(message.chat.id, "С какого вы города")
            bot.register_next_step_handler(message, get_city)
        except:
            bot.send_message(message.chat.id, "Вы должны отправить возраст")
            bot.register_next_step_handler(message, get_age)
            return

def get_city(message):
    if message.content_type == "text":
        tmp_user_info[message.from_user.id].append(message.text)
        bot.send_message(message.chat.id, "Введите описание анкеты")
        bot.register_next_step_handler(message, get_description)
    else:
        bot.send_message(message.chat.id, "Вы должны отправить мне текст")
        bot.register_next_step_handler(message, get_city)

def get_description(message):
    if message.content_type == "text":
        if len(message.text) > 100:
            bot.send_message(message.chat.id, "Слишком много текста, сократите его")
            bot.register_next_step_handler(message, get_description)
            return
        tmp_user_info[message.from_user.id].append(message.text)
        bot.send_message(message.chat.id, "Отправьте фотографию")
        bot.register_next_step_handler(message, get_photo)
    else:
        bot.send_message(message.chat.id, "Вы должны отправить мне текст")
        bot.register_next_step_handler(message, get_description)

def get_photo(message):
    if message.content_type == "photo":
        new_file = bot.get_file(message.photo[-1].file_id)
        downloaded_photo = bot.download_file(new_file.file_path)

        tmp_user_info[message.from_user.id].append(downloaded_photo)
        
        show_questionnaire(message)
    else:
        bot.send_message(message.chat.id, "Вы должны отправить фотографию")
        bot.register_next_step_handler(message, get_photo)

# Пока не нужно
"""
def show_questionnaire_with_many_photos(message):
    qu_photos = tmp_user_info[message.from_user.id][-1]
    user_info = tmp_user_info[message.from_user.id][:-1]
    print(qu_photos)

    # TODO: Сделать создание всей этой формы в отдельной функции

    qu_text = f"{user_info[0]}, {user_info[1]}, {user_info[2]}\n{user_info[3]}"

    for cnt in range(len(qu_photos)):
        if cnt == 0:
            qu_photos[cnt] = types.InputMediaPhoto(qu_photos[cnt], caption=qu_text)
        else:
            qu_photos[cnt] = types.InputMediaPhoto(qu_photos[cnt])

    bot.send_media_group(message.chat.id, qu_photos)
    bot.send_message(message.chat.id, "Подтвердить?")
    bot.register_next_step_handler(message, submit_questionnaire)
"""

def show_questionnaire(message):
    photo = tmp_user_info[message.from_user.id][-1]
    user_info = tmp_user_info[message.from_user.id][:-1]

    qu_text = f"{user_info[0]}, {user_info[1]}, {user_info[2]}\n{user_info[3]}"

    bot.send_photo(message.chat.id, photo, qu_text)
    bot.send_message(message.chat.id, "Подтвердить?")
    bot.register_next_step_handler(message, submit_questionnaire)

def submit_questionnaire(message):
    if message.text == "Да":
        result = insert_questionnaire(message, tmp_user_info[message.from_user.id])
        if result:
            bot.send_message(message.chat.id, "Анкета успешно создана", reply_markup=main_keyboard)
        else:
            bot.send_message(message.chat.id, "Во время создания анкеты произошла ошибка")
        return
    else:
        pass

# @bot.message_handler(content_types=["photo"])
# def handle_photo(message):
#     bot.send_message(message.chat.id, "Принял фото")

def accept_questionnaire_removal(message):
    # Не удалять анкету если пользователь написал "нет" или что угодно, кроме да
    if not message.content_type == "text":
        bot.register_next_step_handler(message, accept_questionnaire_removal)
    if message.text.lower() == "да":
        user_id = message.from_user.id
        result = remove_questionnaire(user_id)
        if (result):
            bot.send_message(message.chat.id, "Анкета была удалена", reply_markup=main_keyboard)
        else:
            bot.send_message(message.chat.id, "Во время удаления анкеты произошла ошибка")
    elif message.text.lower() == "нет":
        pass
    else:
        bot.register_next_step_handler(message, accept_questionnaire_removal)

def remove_questionnaire(user_id):
    try:
        with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            cursor = connection.cursor()

            cursor.execute(f"DELETE FROM Questionnaires WHERE UserID = {int(user_id)}")
            connection.commit()

            return True
    except Exception as e:
        print(e)
        return False

def switch_mutual_like(message, mutual_likes, current_id):
    if message.text == "Предыдущая" or message.text == "Следующая":
        if message.text == "Предыдущая" and current_id > 0:
            current_id -= 1
        elif message.text == "Следующая" and current_id < len(outgoing_likes):
            current_id += 1
        else:
            return

        try:
            with connect(
                host="localhost",
                user="mezzano",
                password="23561423",
                database='Tindergram'
            ) as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(mutual_likes[current_id][0])}")
                current_mutual_like = cursor.fetchone()[0]


                formatted_qu = format_questionnaire(current_mutual_qu)

                if current_id > 0 and current_id < len(mutual_likes) - 1:
                    keybrd = next_prev_keyboard
                elif current_id > 0:
                    keybrd = prev_keyboard
                elif current_id < len(mutual_likes) - 1:
                    keybrd = next_keyboard
                else:
                    keybrd = exit_keyboard

                bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"] + "\n\n" + current_mutual_qu[5], reply_markup=keybrd)
                bot.register_next_step_handler(message, switch_mutual_like, mutual_likes, current_id)
                

        except Exception as e:
            print(e)
            return

        
    elif message.text == "Выход":
        bot.send_message(message.from_user.id, "Главное меню", reply_markup=main_keyboard)
    else:
        bot.register_next_step_handler(message, switch_mutual_like, mutual_likes, current_id)


# TODO
def switch_outgoing_like(message, outgoing_likes, current_id):
    if message.text == "Предыдущая" or message.text == "Следующая":
        if message.text == "Предыдущая" and current_id > 0:
            current_id -= 1
        elif message.text == "Следующая" and current_id < len(outgoing_likes):
            current_id += 1
        else:
            return

        try:
            with connect(
                host="localhost",
                user="mezzano",
                password="23561423",
                database='Tindergram'
            ) as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(outgoing_likes[current_id][0])}")
                current_outgoing_like = cursor.fetchone()


                formatted_qu = format_questionnaire(current_outgoing_like)

                if current_id > 0 and current_id < len(outgoing_likes) - 1:
                    keybrd = next_prev_keyboard
                elif current_id > 0:
                    keybrd = prev_keyboard
                elif current_id < len(outgoing_likes) - 1:
                    keybrd = next_keyboard
                else:
                    keybrd = exit_keyboard

                bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"], reply_markup=keybrd)
                bot.register_next_step_handler(message, switch_outgoing_like, outgoing_likes, current_id)
                

        except Exception as e:
            print(e)
            return

        
    elif message.text == "Выход":
        bot.send_message(message.from_user.id, "Главное меню", reply_markup=main_keyboard)
    else:
        bot.register_next_step_handler(message, switch_outgoing_like, outgoing_likes, current_id)

def insert_mutual_like(first_user, second_user):
    try:
        with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO MutualLikes(FirstUserID, SecondUserID) VALUES(%s, %s)"
            vals = (first_user, second_user)
            cursor.execute(query, vals)
            connection.commit()

            return True

    except Exception as e:
        print(e)
        return False

def remove_from_likes(sender_id, recipient_id):
    try:
        with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM Likes WHERE Sender={sender_id} AND Recipient={recipient_id}")
            connection.commit()

            return True
            

    except Exception as e:
        print(e)
        return False

def switch_incoming_like(message, incoming_likes):
    is_empty = lambda lst: len(lst) == 0

    if message.text == "Лайк" or message.text == "Пропустить":
        current_incoming_like = incoming_likes[0][0]
        incoming_likes = [like for like in incoming_likes if not like[0] == current_incoming_like]

        if message.text == "Лайк":
            result = insert_mutual_like(message.from_user.id, current_incoming_like)
            if result:
                remove_from_likes(sender_id=current_incoming_like, recipient_id=message.from_user.id)

                bot.send_message(current_incoming_like, "У вас взаимный лайк")
                user_link = get_user_with_link(current_incoming_like)
                bot.send_message(message.from_user.id, "Удачного общения\n" + user_link)
                if is_empty(incoming_likes):
                    bot.send_message(message.from_user.id, "Вы ответили на все лайки", reply_markup=main_keyboard)
                    return
                else:
                    try:
                        with connect(
                            host="localhost",
                            user="mezzano",
                            password="23561423",
                            database='Tindergram'
                        ) as connection:
                            cursor = connection.cursor()
                            cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(current_incoming_like)}")
                            current_incoming_qu = cursor.fetchone()

                            formatted_qu = format_questionnaire(current_incoming_qu)

                            bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"], reply_markup=like_skip_keyboard)
                            bot.register_next_step_handler(message, switch_incoming_like, incoming_likes)

                    except Exception as e:
                        print(e)
                        bot.send_message(message.from_user.id, "Произошла ошибка", reply_markup=main_keyboard)
                        return
                        return False
            
        elif message.text == "Пропустить":
            result = remove_from_likes(sender_id=current_incoming_like, recipient_id=message.from_user.id)
            if result:
                if is_empty(incoming_likes):
                    bot.send_message(message.from_user.id, "Вы ответили на все входящие лайки", reply_markup=main_keyboard)
                    return
                else:
                    try:
                        with connect(
                            host="localhost",
                            user="mezzano",
                            password="23561423",
                            database='Tindergram'
                        ) as connection:
                            cursor = connection.cursor()
                            cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(current_incoming_like)}")
                            current_incoming_qu = cursor.fetchone()

                            formatted_qu = format_questionnaire(current_incoming_qu)

                            bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"], reply_markup=like_skip_keyboard)
                            bot.register_next_step_handler(message, switch_incoming_like, incoming_likes)

                    except Exception as e:
                        print(e)
                        return False
            else:
                bot.send_message(message.from_user.id, "Произошла ошибка", reply_markup=main_keyboard)
                return
    else:
        bot.send_message(message.from_user.id, "Я Вас не понял")
        bot.register_next_step_handler(message, switch_incoming_like, incoming_likes)
    

# TEST
def like_questionnaire(sender_id, recipient_id):
    try:
        with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            cursor = connection.cursor()

            cursor.execute(f"SELECT * FROM Likes WHERE Sender = {sender_id} AND Recipient = {recipient_id}")
            print(True)
            is_not_unique = cursor.fetchall()

            if is_not_unique:
                return False

            query = ("INSERT INTO Likes(Sender, Recipient) VALUES(%s, %s)")
            vals = (int(sender_id), int(recipient_id))
            cursor.execute(query, vals)
            connection.commit()

            return True
    except Exception as e:
        print(e)
        return False

@bot.message_handler(content_types=["text"])
def input_handler(message):
    print("chat id", message.chat.id)
    print(f't.me/{message.chat.username}/{message.from_user.id}')
    print(message.from_user.username)
    global current_qu

    if not user_is_initialized(message.from_user.id):
        return

    
    if message.text == "Анкеты":
        current_qu = get_random_questionnaire(message.from_user.id)

        if current_qu == {}:
            bot.send_message(message.chat.id, "К сожалению, на данный момент анкет нет")
            return
        
        bot.send_photo(message.chat.id, current_qu["photo"], current_qu["text"], reply_markup=questionnaire_keyboard)

    elif message.text == "Лайк" or message.text == "Скип":
        if current_qu == None:
            return
        if message.text == "Лайк":
            result = like_questionnaire(message.from_user.id, current_qu["user_id"])

            if result:
                bot.send_message(current_qu["user_id"], "У вас новый лайк")

        current_qu = get_random_questionnaire(message.from_user.id)
        
        bot.send_photo(message.chat.id, current_qu["photo"], current_qu["text"], reply_markup=questionnaire_keyboard)

    elif message.text == "Главное меню":
        bot.send_message(message.chat.id, "Главное меню", reply_markup=main_keyboard)

    elif message.text == "Профиль":
        user_id = message.from_user.id
        profile_info = get_profile_info(user_id)
        bot.send_photo(message.chat.id, profile_info["photo"], profile_info["text"], reply_markup=profile_keybaord)

    elif message.text == "Удалить анкету":
        bot.send_message(message.chat.id, "Вы уверены?", reply_markup=yes_no_keyboard)
        bot.register_next_step_handler(message, accept_questionnaire_removal)

    elif message.text == "Исходящие лайки":
        '''
        Выбирает все анкеты и возвращает первую анкету
        Передаёт управление "свитчеру" анкет
        '''
        try:
            with connect(
                host="localhost",
                user="mezzano",
                password="23561423",
                database='Tindergram'
            ) as connection:
                bot.send_message(message.from_user.id, "Исходящие лайки")
                cursor = connection.cursor()

                cursor.execute(f"SELECT Recipient FROM Likes WHERE Sender = {int(message.from_user.id)}")
                outgoing_likes = cursor.fetchall()
                if not outgoing_likes:
                    bot.send_message(message.from_user.id, "У вас пока ещё нет исходящих лайков")
                    return 
                

                # КОСТЫЛЬ
                # Достаём все поля, чтобы функция вернула правильное значение
                cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(outgoing_likes[0][0])}")
                current_outgoing_like = cursor.fetchone()

                formatted_qu = format_questionnaire(current_outgoing_like)
                
                current_id = 0
                if current_id > 0 and current_id < len(outgoing_likes) - 1:
                    keybrd = next_prev_keyboard
                elif current_id > 0:
                    keybrd = prev_keyboard
                elif current_id < len(outgoing_likes) - 1:
                    keybrd = next_keyboard
                else:
                    keybrd = exit_keyboard

                bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"], reply_markup=keybrd)

                bot.register_next_step_handler(message, switch_outgoing_like, outgoing_likes, current_id)
        except Exception as e:
            print(e)

    elif message.text == "Входящие лайки":
        try:
            with connect(
                host="localhost",
                user="mezzano",
                password="23561423",
                database='Tindergram'
            ) as connection:
                cursor = connection.cursor()

                cursor.execute(f"SELECT Sender FROM Likes WHERE Recipient = {int(message.from_user.id)}")
                incoming_likes = cursor.fetchall()
                if not incoming_likes:
                    bot.send_message(message.from_user.id, "У вас пока ещё нет входящих лайков")
                    return 
                
                bot.send_message(message.from_user.id, "Входящие лайки")
                cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(incoming_likes[0][0])}")
                current_incoming_like = cursor.fetchone()

                formatted_qu = format_questionnaire(current_incoming_like)

                bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"], reply_markup=like_skip_keyboard)

                bot.register_next_step_handler(message, switch_incoming_like, incoming_likes)
        except Exception as e:
            print(e)

    elif message.text == "Взаимные лайки":
        try:
            with connect(
                host="localhost",
                user="mezzano",
                password="23561423",
                database='Tindergram'
            ) as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT FirstUserID FROM MutualLikes WHERE SecondUserID = {message.from_user.id}")
                left_likes = cursor.fetchall()
                cursor.execute(f"SELECT SecondUserID FROM MutualLikes WHERE FirstUserID = {message.from_user.id}")
                right_likes = cursor.fetchall()

                mutual_likes = left_likes + right_likes

                if not mutual_likes:
                    bot.send_message(message.from_user.id, "У вас пока ещё нет взаимных лайков")
                    return

                current_mutual_like = mutual_likes[0][0]
                cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = {int(current_mutual_like)}")
                current_mutual_qu = cursor.fetchone()
                current_id = 0

                if current_id > 0 and current_id < len(mutual_likes) - 1:
                    keybrd = next_prev_keyboard
                elif current_id > 0:
                    keybrd = prev_keyboard
                elif current_id < len(mutual_likes) - 1:
                    keybrd = next_keyboard
                else:
                    keybrd = exit_keyboard

                formatted_qu = format_questionnaire(current_mutual_qu)
                bot.send_photo(message.from_user.id, formatted_qu["photo"], formatted_qu["text"] + "\n\n" + current_mutual_qu[5], reply_markup=keybrd)

                bot.register_next_step_handler(message, switch_mutual_like, mutual_likes, current_id)

        except Exception as e:
            print(e)
            return False
        

bot.set_update_listener(messages_handler)
bot.infinity_polling()