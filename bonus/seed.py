import time

import mysql.connector
from werkzeug.security import generate_password_hash


for attempt in range(30):
    try:
        connection = mysql.connector.connect(
            host="mysql",
            user="app_user",
            password="app1234",
            database="login_db",
        )
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE username = %s", ("student",))

        if cursor.fetchone() is None:
            password_hash = generate_password_hash("1234")
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                ("student", password_hash),
            )
            connection.commit()

        cursor.close()
        connection.close()
        break
    except mysql.connector.Error:
        if attempt == 29:
            raise
        time.sleep(1)
