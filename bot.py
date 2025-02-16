from flask import Flask, request
import requests
import openai
import os

# Pobieramy zmienne środowiskowe (Render nie lubi trzymania haseł w kodzie)
TOKEN = 7930835004:AAF9hXnDNVpsSRLPP7N-kIaYC3GW-r0YriA ("TELEGRAM_TOKEN")
OPENAI_API_KEY = "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"("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

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
