from flask import Flask, request
import requests
import openai
import os


# Pobieranie kluczy API z zmiennych środowiskowych
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("Brak klucza API! Upewnij się, że dodałeś zmienne środowiskowe w Render.")

# Teraz możesz używać tych zmiennych w kodzie
print(f"OpenAI API Key: {OPENAI_API_KEY[:5]}...")  # Podgląd (bezpieczny skrót)
print(f"Telegram Bot Token: {TELEGRAM_BOT_TOKEN[:5]}...")


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot działa! 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # Wysyłamy zapytanie do OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "Jesteś doradcą od wykończenia wnętrz."},
                      {"role": "user", "content": text}]
        )
        reply = response["choices"][0]["message"]["content"]

        # Wysyłamy odpowiedź do użytkownika
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                      json={"chat_id": chat_id, "text": reply})

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
