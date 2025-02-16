import os
import requests
import openai
from flask import Flask, request, jsonify

# Pobieranie kluczy API z zmiennych środowiskowych
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("Brak klucza API! Upewnij się, że dodałeś zmienne środowiskowe w Render.")

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot działa! 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Otrzymana wiadomość:", data)  # Debugowanie

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # Generowanie odpowiedzi przez OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Jesteś doradcą od wykończenia wnętrz."},
                {"role": "user", "content": text}
            ],
            api_key=OPENAI_API_KEY  # Klucz API OpenAI
        )
        reply = response["choices"][0]["message"]["content"]

        # Wysłanie odpowiedzi do użytkownika
        send_message(chat_id, reply)

    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    """Funkcja wysyłająca wiadomość do użytkownika przez API Telegrama"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    
    response = requests.post(url, json=payload)
    print("Odpowiedź API Telegrama:", response.json())  # Debugowanie

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
