import os
import threading
from flask import Flask
import telebot
from google import genai

# Server botni o'chib qolmasligi uchun kichik veb-xizmat
app = Flask(__name__)

@app.route('/')
def home():
    return "Gemini Bot 24/7 ishlab turibdi!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Botingiz sozlamalari
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Assalomu alaykum! Men 24/7 rejimda ishlovchi Gemini botiman. Savolingizni bering.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

if __name__ == "__main__":
    # Veb-xizmatni alohida oqimda ishga tushirish
    threading.Thread(target=run_web, daemon=True).start()
    # Botni ishga tushirish
    bot.infinity_polling()
