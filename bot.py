import telebot
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("API_KEY")
print(API_KEY)

bot=telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start','greet'])
def greet(message):
    bot.reply_to(message,"Hello! Welcome to your personal Trader Buddy")

bot.polling()