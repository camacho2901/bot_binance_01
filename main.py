from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🟢 Token y chat ID de Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "6920302085:AAHRoc_dmnFHTkAUwK_f3ayT3LZpgwRX6zg")
TELEGRAM_USER_ID = os.environ.get("TELEGRAM_USER_ID", "1162543748")

# 🟢 URL de la API de Telegram
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route("/")
def home():
    return "Bot de Telegram funcionando correctamente ✅"

@app.route("/mensaje", methods=["POST"])
def enviar_mensaje():
    try:
        data = request.get_json()
        mensaje = data.get("mensaje")

        if not mensaje:
            return jsonify({"error": "Falta el campo 'mensaje'"}), 400

        payload = {
            "chat_id": TELEGRAM_USER_ID,
            "text": mensaje
        }

        response = requests.post(TELEGRAM_API_URL, json=payload)

        if response.ok:
            return jsonify({"estado": "enviado", "respuesta": response.json()}), 200
        else:
            return jsonify({"estado": "error", "respuesta": response.text}), 500

    except Exception as e:
        return jsonify({"estado": "error", "mensaje": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
