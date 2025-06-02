import json
import requests
import time
from flask import Flask
from threading import Thread

with open("config.json") as f:
    config = json.load(f)

TOKEN = config["telegram_token"]
CHAT_ID = config["telegram_user_id"]
MONEDAS = config["monedas"]
INTERVALO = config["intervalo_segundos"]
LIMITES = config["limites"]

def enviar_mensaje(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def obtener_ofertas(moneda, tipo):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "asset": moneda,
        "fiat": "BOB",
        "tradeType": tipo,
        "page": 1,
        "rows": 1,
        "payTypes": [],
        "publisherType": None
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"]
    except Exception as e:
        print("Error al obtener ofertas:", e)
    return []

def bot():
    while True:
        for moneda in MONEDAS:
            for tipo in ["BUY", "SELL"]:
                ofertas = obtener_ofertas(moneda, tipo)
                if ofertas:
                    precio = float(ofertas[0]["adv"]["price"])
                    limite = LIMITES[moneda]["buy_max"] if tipo == "BUY" else LIMITES[moneda]["sell_min"]
                    if (tipo == "BUY" and precio <= limite) or (tipo == "SELL" and precio >= limite):
                        nombre = ofertas[0]["advertiser"]["nickName"]
                        enlace = f"https://p2p.binance.com/es/advertiserDetail?advertiserNo={ofertas[0]['advertiser']['userNo']}"
                        msg = f"💱 *{tipo}* oferta de *{moneda}*
👤 Vendedor: {nombre}
💰 Precio: *{precio} Bs.*
🔗 [Ver Oferta]({enlace})"
                        enviar_mensaje(msg)
        time.sleep(INTERVALO)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot activo", 200

def run_web():
    app.run(host='0.0.0.0', port=3000)

if __name__ == "__main__":
    Thread(target=bot).start()
    Thread(target=run_web).start()
