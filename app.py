from flask import Flask, request, jsonify
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
    requests.post(url, json=payload, timeout=15)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    symbol = data.get("symbol", "US100")
    action = data.get("action", "SIGNAL")
    entry = data.get("entry", "")
    sl = data.get("sl", "")
    tp1 = data.get("tp1", "")
    tp2 = data.get("tp2", "")
    tp3 = data.get("tp3", "")

    side_emoji = "🟢" if action.upper() == "BUY" else "🔴"

    message = (
        f"{side_emoji} {symbol} {action}\n\n"
        f"Entry : {entry}\n"
        f"Stop : {sl}\n\n"
        f"🎯 TP1 : {tp1}\n"
        f"🎯 TP2 : {tp2}\n"
        f"🎯 TP3 : {tp3}"
    )

    send_telegram(message)
    return jsonify({"status": "ok"}), 200


@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
