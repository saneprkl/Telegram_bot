import os

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from datetime import datetime
import jokes
import asyncio
import time

from keep_alive import keep_alive

API_KEY = os.environ['API_KEY']
BOT_NAME = []
BOT_NAME.append(os.environ['BOT_NAME'])
BOT_NAME.append(os.environ['BOT_NAME_ALT'])


def greet(update, context):
  update.message.reply_text("Greetings")


def help(update, context):
  update.message.reply_text("No can do")

async def handle_response(text: str) -> str:
  if text in ('joke', 'tell a joke'):
    joke = await jokes.tell_joke()
    if len(joke) == 1:
      return str(joke[2:-2])
    if len(joke) == 2:
      return joke
        
  if text in ('hey', 'hi', 'hello', 'lo'):
    return 'Well hello there'
  if 'how are you' in text:
    return 'Im all good, thanks'
  if text in ('date', 'date?', 'time', 'time?'):
    dateNow = datetime.now()
    date = dateNow.strftime('%d/%m/%y, %H:%M:%S @GMT +00:00')
    return str(date)

  return await 'What?'


def handle_message(update, context):
  message_type = update.message.chat.type
  text = str(update.message.text).lower()
  response = ''
  #print(f'User ({update.message.chat.id}) says:"{text}" in: {message_type}')

  if message_type == 'group':
    print(
      f'Group chat id ({update.message.chat.id}) says:"{text}" in: {message_type}'
    )
    for i in BOT_NAME:
      if i in text:
        new_text = text.replace('@' + i, '').strip()
        response = asyncio.run(handle_response(new_text))
  else:
    print(f'User ({update.message.chat.id}) says:"{text}" in: {message_type}')
    response = asyncio.run(handle_response(text))
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
