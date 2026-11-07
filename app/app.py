import datetime
import os
import secrets
import socket
import string

import psycopg
from flask import Flask, abort, jsonify, redirect, request

app = Flask(__name__)
ALPHABET = string.ascii_letters + string.digits


def get_conn():
    # Thông tin kết nối lấy từ biến môi trường (ConfigMap + Secret)
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        dbname=os.environ.get("DB_NAME", "postgres"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
        connect_timeout=3,
        autocommit=True,
    )


def init_db():
    # IF NOT EXISTS: chạy nhiều lần cũng không lỗi
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS links ("
            " code TEXT PRIMARY KEY,"
            " url TEXT NOT NULL,"
            " hits INTEGER NOT NULL DEFAULT 0)"
        )


@app.get("/")
def index():
    return "Hello from k8s-gitops-homelab. I'm KidPcongg, nice to meet you!"


@app.get("/healthz")
def healthz():
    # Liveness: chỉ kiểm tra process còn sống, KHÔNG phụ thuộc DB
    return jsonify(status="ok")


@app.get("/readyz")
def readyz():
    # Readiness: chỉ sẵn sàng khi kết nối được DB
    try:
        init_db()
        return jsonify(status="ready")
    except psycopg.Error:
        return jsonify(status="db unavailable"), 503


@app.get("/api/info")
def info():
    return jsonify(
        hostname=socket.gethostname(),
        version=os.environ.get("APP_VERSION", "dev"),
    )


@app.get("/api/time")
def get_time():
    return jsonify(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@app.post("/api/links")
def create_link():
    data = request.get_json(silent=True) or {}
    url = str(data.get("url", "")).strip()
    if not url.startswith(("http://", "https://")):
        return jsonify(error="url must start with http:// or https://"), 400
    code = "".join(secrets.choice(ALPHABET) for _ in range(6))
    with get_conn() as conn:
        # %s là tham số an toàn, chống SQL injection, KHÔNG ghép chuỗi
        conn.execute("INSERT INTO links (code, url) VALUES (%s, %s)", (code, url))
    return jsonify(code=code, created_by=socket.gethostname()), 201


@app.get("/api/links/<code>")
def get_link(code):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT url, hits FROM links WHERE code = %s", (code,)
        ).fetchone()
    if row is None:
        abort(404)
    return jsonify(code=code, url=row[0], hits=row[1], served_by=socket.gethostname())


@app.get("/s/<code>")
def follow(code):
    with get_conn() as conn:
        row = conn.execute(
            "UPDATE links SET hits = hits + 1 WHERE code = %s RETURNING url", (code,)
        ).fetchone()
    if row is None:
        abort(404)
    return redirect(row[0], code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)