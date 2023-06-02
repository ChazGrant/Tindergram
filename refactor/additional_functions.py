from mysql.connector import connect
import random

get_user_link = lambda username: f"t.me/{username}"


def format_questionnaire(user_info):
    text = f"{user_info[0]} {user_info[1]}, {user_info[2]}\n{user_info[3]}"
    photo = user_info[6]

    return {
        "text" : text,
        "photo": photo,
        "user_id": user_info[5]
    }
