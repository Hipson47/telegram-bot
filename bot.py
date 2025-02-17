from flask import Flask, request
import os
import telebot
import openai

# Pobranie zmiennych środowiskowych
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RAILWAY_URL = os.getenv("RAILWAY_URL")
PORT = int(os.getenv("PORT", 5000))

# Konfiguracja OpenAI
openai.api_key = OPENAI_API_KEY

# Inicjalizacja bota i aplikacji Flask
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "ok", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Obsługa wiadomości - odpowiadanie przy użyciu OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Jesteś pomocnym asystentem."},
                      {"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response['choices'][0]['message']['content'])
    except Exception as e:
        bot.reply_to(message, "Wystąpił błąd, spróbuj ponownie.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RAILWAY_URL}/webhook")
    app.run(host="0.0.0.0", port=PORT)
