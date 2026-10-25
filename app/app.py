from flask import Flask, jsonify
import socket
import datetime
import os

app = Flask(__name__)

@app.get("/")
def index():
    return "Hello from k8s-gitops-homelab. I'm KidPcongg, nice to meet you!"

@app.get("/healthz")
def healthz():
    return jsonify(status="ok")

@app.get("/api/info")
def info():
    return jsonify(hostname=socket.gethostname(), version=os.environ.get("APP_VERSION", "dev"),)

@app.get("/api/time")
def get_time():
    return jsonify(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)