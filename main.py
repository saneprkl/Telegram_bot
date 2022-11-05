import os
import telebot
from keep_alive import keep_alive

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Wassup")


keep_alive()
bot.polling()
