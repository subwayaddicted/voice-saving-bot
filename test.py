from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

updater = Updater(token='968628814:AAEyjjPinThWqec11sikYgNzvoxo6JZu3PU', use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)


# Functions
def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()