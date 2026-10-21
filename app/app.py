from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.get("/")
def index():
    return "Hello from k8s-gitops-homelab !"

@app.get("/healthz")
def healthz():
    return jsonify(status = "Ok")

@app.get("/api/info")
def info():
    return jsonify(hostname = socket.gethostname())

@app.get("/api/time")
def time():
    return jsonify(time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000)