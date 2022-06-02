from telebot import types

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