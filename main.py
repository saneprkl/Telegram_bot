import os

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from datetime import datetime

from keep_alive import keep_alive

API_KEY = os.environ['API_KEY']
BOT_NAME = []
BOT_NAME.append(os.environ['BOT_NAME'])
BOT_NAME.append(os.environ['BOT_NAME_ALT'])


def greet(update, context):
  update.message.reply_text("Greetings")


def help(update, context):
  update.message.reply_text("No can do")


def handle_response(text: str) -> str:
  if text in ('hey', 'hi', 'hello', 'lo'):
    return 'Well hello there'
  if 'how are you' in text:
    return 'Im all good, thanks'
  if text in ('date', 'date?', 'time', 'time?'):
    dateNow = datetime.now()
    date = dateNow.strftime('%d/%m/%y, %H:%M:%S')
    return str(date)

  return 'What?'


def handle_message(update, context):
  message_type = update.message.chat.type
  text = str(update.message.text).lower()
  response = ''

  #print(f'User ({update.message.chat.id}) says:"{text}" in: {message_type}')

  if message_type == 'group':
    print(
      f'Group chat id ({update.message.chat.id}) says:"{text}" in: {message_type}'
    )
    if text in BOT_NAME:
      print('Tagging the bot recognized *******************************')
    # new_text = text.replace(BOT_NAME, '').strip()
    #response = handle_response(new_text)
  else:
    print(f'User ({update.message.chat.id}) says:"{text}" in: {message_type}')
    response = handle_response(text)
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
