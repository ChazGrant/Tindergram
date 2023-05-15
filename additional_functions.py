from mysql.connector import connect


get_user_link = lambda username: f"t.me/{username}"


def get_random_questionnaire(current_user_id):
    all_questionnaires = get_all_questionnaires(current_user_id)
    # Если анкет нет
    if not all_questionnaires:
        return dict()
    user_info = random.choice(all_questionnaires)

    profile_info = format_questionnaire(user_info)

    return profile_info

def format_questionnaire(user_info):
    text = f"{user_info[0]} {user_info[1]}, {user_info[2]}\n{user_info[3]}"
    photo = user_info[6]

    return {
        "text" : text,
        "photo": photo,
        "user_id": user_info[5]
    }

class Database:
    def __init__(self):
        ...

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

    def get_next_mutual_like(user_id):
        try:
            with connect(
                host="localhost",
                user="mezzano",
                password="23561423",
                database='Tindergram'
            ) as connection:
                cursor = connection.cursor()
                cursor.execute(f"SELECT Name, Age, City, Description, UserID, UserLink, Photo FROM Questionnaires WHERE UserID = ?", (user_id, ))
                next_mutual_like = cursor.fetchone()[0]

                return next_mutual_like
        except Exception as e:
            print(str(e))
            return 0

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