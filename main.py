import os

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from datetime import datetime
from pprint import pprint
import jokes
import weather_api
import forecast
import asyncio
import time

from keep_alive import keep_alive

API_KEY = os.environ['API_KEY']
BOT_NAME = []
BOT_NAME.append(os.environ['BOT_NAME'])
BOT_NAME.append(os.environ['BOT_NAME_ALT'])

# /greet command
def greet(update, context):
  update.message.reply_text("Greetings")

# /help command
def help(update, context):
  help_message = f"You can talk to the bot by tagging it with @{BOT_NAME[0]} or @{BOT_NAME[1]} \
    \n\nIt can tell jokes:\ne.g. --> @{BOT_NAME[0]} joke \
      \n\nYou can get the current weather around the world based on a city:\ne.g. --> @{BOT_NAME[0]} weather helsinki"
  update.message.reply_text(help_message)

weather_symbols = {
  "Snow": "\U0001F328",
  "Clouds": "\U00002601",
  "Rain": "\U00002614",
  "Drizzle": "\U00002614",
  "Thunderstorm": "\U000026A1",
  "Mist": "\U0001F32B",
  "Clear": "\U00002600",
  "Fog": "\U0001F32B"
}
# Get weather by city
def getWeather(text):
  symbol = ""
  city = text.replace("weather ", "")
  print("weather recognized -->", city)
  weather = weather_api.weather_city(city)
  pprint(weather)
  if weather[7] in weather_symbols:
    symbol = weather_symbols[weather[7]]
  current_weather = f"Weather in {weather[0]}\nTemperature {weather[1]} °C\n{weather[7]} {symbol}\nWind speed {weather[2]} m/s\nHumidity {weather[3]}%\nSunrise {weather[4]}\nSunset {weather[5]}\nLength of day is {weather[6]}"
  return current_weather

# Handles the response to user input
async def handle_response(text: str, update) -> str:
  if text in ('joke', 'tell a joke'):
    joke = await jokes.tell_joke()
    if len(joke) == 2:
      print("2 parter", joke)
      j = ' '.join(joke)
      return j
        
    print("single", joke)
    return joke

  if text.startswith("weather ") == True:
    return getWeather(text)
  if text.startswith("forecast ") == True:
    print("found")
    return forecast.forecast(text)
  if text in ('hey', 'hi', 'hello', 'lo'):
    return f'Well hello there {update.message.chat.first_name}'
  if 'how are you' in text:
    return 'Im all good, thanks'
  if text in ('date', 'date?', 'time', 'time?'):
    dateNow = datetime.now()
    date = dateNow.strftime('%d/%m/%y, %H:%M:%S @GMT +00:00')
    return str(date)
  return 'What?'


def handle_message(update, context):
  message_type = update.message.chat.type
  text = str(update.message.text).lower()
  response = ''
  #print(f'User ({update.message.chat.id}) says:"{text}" in: {message_type}')

  # Check if message in group chat
  if message_type == 'group':
    print(
      f'Group chat id ({update.message.chat.id}) says:"{text}" in: {message_type}'
    )
    for i in BOT_NAME:
      if i in text:
        new_text = text.replace('@' + i, '').strip()
        response = asyncio.run(handle_response(new_text, update))
        
  # Else message will be in private chat
  else:
    print(f'User ({update.message.chat.id}) says:"{text}" in: {message_type}')
    response = asyncio.run(handle_response(text, update))
  update.message.reply_text(response)


def error(update, context):
  print(f'Update {update} caused error: {context.error}')


if __name__ == '__main__':
  updater = Updater(API_KEY, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler('greet', greet))
  dp.add_handler(CommandHandler('help', help))

  dp.add_handler(MessageHandler(Filters.text, handle_message))
  dp.add_error_handler(error)

keep_alive()
updater.start_polling()
