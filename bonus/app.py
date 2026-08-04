import json
import os
import secrets
from datetime import datetime

import mysql.connector
import redis
from flask import Flask, jsonify, redirect, request
from werkzeug.security import check_password_hash


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


def mode_info():
    mode = os.getenv("APP_MODE", "normal")  # 환경변수가 없으면 normal을 사용한다.
    if mode == "maintenance":
        mode_message = "현재 서비스 점검 중입니다."
    else:
        mode_message = "서비스를 이용할 수 있습니다."
    return mode, mode_message


def login_page(message="로그인하세요.", show_alert=False):
    mode, mode_message = mode_info()
    alert_script = ""
    if show_alert:
        alert_script = '<script>alert("서비스 점검 중이므로 로그인할 수 없습니다.");</script>'
    return f"""
    <h1>My First Compose</h1>
    <p>{mode_message}</p>
    <p>{message}</p>
    <form method="post">
      <input name="username" placeholder="아이디">
      <input name="password" type="password" placeholder="비밀번호">
      <button type="submit">로그인</button>
    </form>
    <p>mode={mode}</p>
    {alert_script}
    """


def main_page(username, message):
    mode, mode_message = mode_info()
    return f"""
    <h1>메인 화면</h1>
    <p>{mode_message}</p>
    <p>{username}님, 환영합니다.</p>
    <p>{message}</p>
    <p>로그아웃까지 남은 시간: <span id="remaining">10</span>초</p>
    <p>페이지를 새로고침하면 세션이 10초 연장됩니다.</p>
    <p>mode={mode}</p>
    <script>
      setInterval(async () => {{
        const response = await fetch("/session-ttl");
        const data = await response.json();
        document.getElementById("remaining").textContent = data.remaining;
        if (data.expired) {{
          alert("단시간 이용하지 않아 로그아웃됩니다.");
          location.href = "/";
        }}
      }}, 1000);
    </script>
    """


@app.get("/session-ttl")
def session_ttl():
    token = request.cookies.get("session_token")
    if not token:
        return jsonify(remaining=0, expired=True)

    remaining = redis_client.ttl(f"session:{token}")
    if remaining < 0:
        return jsonify(remaining=0, expired=True)

    return jsonify(remaining=remaining, expired=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if os.getenv("APP_MODE", "normal") == "maintenance":
        if request.method == "POST":
            return login_page("점검 중에는 로그인할 수 없습니다.", show_alert=True)
        return login_page()

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
            response = redirect("/")  # POST 재전송을 막기 위해 GET 메인 화면으로 이동한다.
            response.set_cookie("session_token", token)
            return response

        return login_page("아이디 또는 비밀번호가 틀렸습니다.")

    token = request.cookies.get("session_token")
    if token:
        session_data = redis_client.get(f"session:{token}")
        if session_data:
            redis_client.expire(f"session:{token}", SESSION_TTL)
            username = json.loads(session_data)["username"]
            return main_page(username, "세션이 10초 연장됐습니다.")
        return login_page("세션이 만료되었습니다. 다시 로그인하세요.")

    return login_page()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
