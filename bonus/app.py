import json
import os
import secrets
from datetime import datetime

import mysql.connector
import redis
from flask import Flask, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
SESSION_TTL = 10


def connect_mysql():
    return mysql.connector.connect(
        host="mysql",
        user="app_user",
        password="app1234",
        database="login_db",
    )


redis_client = redis.Redis(host="redis", decode_responses=True)


def prepare_user():
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(username VARCHAR(50) PRIMARY KEY, password_hash VARCHAR(255))"
    )
    cursor.execute("SELECT username FROM users WHERE username = %s", ("student",))
    if cursor.fetchone() is None:
        password_hash = generate_password_hash("1234")
        cursor.execute("INSERT INTO users VALUES (%s, %s)", ("student", password_hash))
        connection.commit()
    cursor.close()
    connection.close()


def login_page(message="로그인하세요."):
    mode = os.getenv("APP_MODE", "study")
    return f"""
    <h1>My First Compose</h1>
    <p>{message}</p>
    <form method="post">
      <input name="username" placeholder="아이디">
      <input name="password" type="password" placeholder="비밀번호">
      <button type="submit">로그인</button>
    </form>
    <p>mode={mode}</p>
    """


@app.route("/", methods=["GET", "POST"])
def index():
    prepare_user()

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        connection = connect_mysql()
        cursor = connection.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row and check_password_hash(row[0], password):
            token = secrets.token_hex(16)
            session_data = json.dumps(
                {"username": username, "login_time": datetime.now().isoformat()}
            )
            redis_client.set(f"session:{token}", session_data, ex=SESSION_TTL)
            response = make_response(login_page("로그인 성공! 10초 세션이 시작됐습니다."))
            response.set_cookie("session_token", token)
            return response

        return login_page("아이디 또는 비밀번호가 틀렸습니다.")

    token = request.cookies.get("session_token")
    if token:
        session_data = redis_client.get(f"session:{token}")
        if session_data:
            redis_client.expire(f"session:{token}", SESSION_TTL)
            username = json.loads(session_data)["username"]
            return login_page(f"{username}님 로그인 중입니다. 세션이 10초 연장됐습니다.")
        return login_page("세션이 만료되었습니다. 다시 로그인하세요.")

    return login_page()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
