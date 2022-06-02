from mysql.connector import connect, Error

try:
    with connect(
            host="localhost",
            user="mezzano",
            password="23561423",
            database='Tindergram'
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT Recipient FROM Likes WHERE Sender = 905463603")
            outgoing_likes = cursor.fetchall()

            print(outgoing_likes[0])
        #all_users = list(map(all_users, lambda lst: lst[0]))

        # print(all_users)

        # photo = open("Igor.jpg", 'rb').read()
        # query = "INSERT INTO Questionnaires (UserID, Name, Age, Description, UserLink, Photo) VALUES (%s, %s, %s, %s, %s, %s)"
        # val = (762815155, "Йигорь", 20, "Молодая легенда в поисках своего Донбасса", "t.me/mezzano", photo)

        # cursor.execute(query, val)
        # connection.commit()
except Error as e:
    print(e)