import random

import telebot
from mysql.connector import Error, connect

from additional_functions import format_questionnaire, get_user_link


class Database(object):
    def __init__(self, host="localhost", username="mezzano", password="23561423", database="Tindergram"):
        self.__connection = connect(
                host=host,
                user=username,
                password=password,
                database=database)
        self._cursor = self.__connection.cursor()

    def __new__(cls, host="localhost", username="mezzano", password="23561423", database="Tindergram"):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def user_is_initialized(self, user_id: int) -> bool:
        # Проверяем есть ли юзер в бд
        self._cursor.execute("SELECT `User_id` FROM Questionnaires")
        all_ids = [item[0] for item in self._cursor.fetchall()]

        if all_ids == []:
            return False
        for user in all_ids:
            if int(user_id) == int(user):
                return True

        return False

    def get_next_mutual_like(self, user_id: int) -> list:
        try:
            self._cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = ?", (user_id, ))
            next_mutual_like = self._cursor.fetchone()[0]

            return next_mutual_like
        except Exception as e:
            print(str(e))
            return []

    def remove_questionnaire(self, user_id: int) -> bool:
        try:
            self._cursor.execute(f"DELETE FROM Questionnaires WHERE UserID = {int(user_id)}")
            self.__connection.commit()

            return True
        except Exception as e:
            print(e)
            return False

    def get_user_with_link(self, user_id: int) -> int:
        try:
            self._cursor.execute(f"SELECT `UserLink` FROM Questionnaires WHERE UserID = {user_id}")
            user_link = self._cursor.fetchone()[0]

            return user_link
        except Exception as e:
            print(e)
            return 0
    
    def get_random_questionnaire(self, current_user_id: int) -> dict:
        all_questionnaires = self.get_all_questionnaires(current_user_id)

        if not all_questionnaires:
            return dict()
        user_info = random.choice(all_questionnaires)

        profile_info = format_questionnaire(user_info)

        return profile_info

    def insert_questionnaire(self, message: telebot.types.Message, credentials: list):
        try:
            user_link = get_user_link(message.from_user.username)
            
            query = "INSERT INTO Questionnaires (UserID, Name, Age, City, Description, Photo, UserLink) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            vals = (int(message.from_user.id), credentials[0], credentials[1], credentials[2], credentials[3], credentials[4], user_link)

            self._cursor.execute(query, vals)

            self.__connection.commit()
            return True
        except Error as e:
            print(e)
            return False

    def get_all_questionnaires(self, current_user_id: int) -> list:
        self._cursor.execute(f"SELECT Name, Age, City, Description, UserLink, UserID, Photo FROM Questionnaires WHERE UserID <> {int(current_user_id)}")
        records = self._cursor.fetchall()

        return records

    def get_profile_info(self, user_id: int) -> list:
        try:
            self._cursor.execute(f"SELECT Name, Age, City, Description, UserLink, UserID, Photo FROM Questionnaires WHERE UserID = {int(user_id)}")
            user_info = self._cursor.fetchone()

            result = format_questionnaire(user_info)

            return result
        except Exception as e:
            print(e)

    def insert_initialized_user(self, user_id):
        query = ("INSERT INTO InitializedUsers (UserID) VALUES (%s)")
        data = (int(user_id), )
        self._cursor.execute(query, data)

        self.__connection.commit()
