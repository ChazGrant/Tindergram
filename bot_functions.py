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

def show_main_menu(u_id):
    print("Main menu for " + str(u_id))

def show_questionnaires(*args):
    print("Here is your questionnaires: ")

def show_profile(*args):
    print("Here is your profile: ")

def show_mutual_likes(*args):
    print("Here is your mutual likes: ")

def show_incoming_likes(*args):
    print("Here is your incoming likes: ")

def show_outcoming_likes(*args):
    print("Here is your outcoming likes: ")

### QUESTIONNAIRE CREATION ###

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

def show_created_questionnaire(message):
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

###                           ###

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

def switch_mutual_like(message, mutual_likes, current_id):
    if message.text == "Предыдущая" or message.text == "Следующая":
        if message.text == "Предыдущая" and current_id > 0:
            current_id -= 1
        elif message.text == "Следующая" and current_id < len(outgoing_likes):
            current_id += 1
        else:
            return
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
    elif message.text == "Выход":
        bot.send_message(message.from_user.id, "Главное меню", reply_markup=main_keyboard)
    else:
        bot.register_next_step_handler(message, switch_mutual_like, mutual_likes, current_id)

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

bot_functions = {
    "главное меню": show_main_menu,
    "анкеты": show_questionnaires,
    "профиль": show_profile,
    "взаимные лайки": show_mutual_likes,
    "входящие лайки": show_incoming_likes,
    "исходящие лайки": show_outcoming_likes
}