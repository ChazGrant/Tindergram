from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="mezzano",
        password="23561423",
        database='Tindergram'
    ) as connection:
        cursor = connection.cursor()
        photo = open("ph.jpg", "rb").read()
        # Проверяем есть ли юзер в бд
        query = "INSERT INTO Questionnaires (UserID, Name, Age, Description, UserLink, Photo, ChatID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        vals = (905463603, "Илллидан", 12, "Молодой Донбасс в поисках своей легенды", "t.me/xavlegbmaofffassssitimi", photo, 905463603)

        cursor.execute(query, vals)

        connection.commit()
except Exception as e:
    print(e)