from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    symbol = data.get("symbol")
    action = data.get("action")
    entry = data.get("entry")
    sl = data.get("sl")
    tp1 = data.get("tp1")
    tp2 = data.get("tp2")
    tp3 = data.get("tp3")

    message = f"""
{action} {symbol}

Entry: {entry}
SL: {sl}

TP1: {tp1}
TP2: {tp2}
TP3: {tp3}
"""

    send_telegram(message)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run()
