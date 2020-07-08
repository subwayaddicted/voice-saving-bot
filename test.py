from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, Filters, CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
import logging, json, mysql.connector

with open("config.json") as json_config:
	data = json.load(json_config)

db = mysql.connector.connect(
	data["mysql"]["host"],
	data["mysql"]["user"],
	data["mysql"]["password"],
	data["mysql"]["db"]
)
db_cursor = db.cursor()

updater = Updater(token=data["telegram"]["token"], use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)


# Functions
def start(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def voice(update: Update, context: CallbackContext):
	voice_id = update.message.voice.file_id
	user_id = update.effective_user.id
	file = context.bot.getFile(update.message.voice.file_id)
	file.download('voice_messages/'+str(user_id)+'__'+voice_id+'.ogg')

	context.bot.send_message(chat_id=update.effective_chat.id, text='Voice saved!')


def unknown(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# Commands handlers
dispatcher.add_handler(CommandHandler('start', start))

# Message Handlers
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

dispatcher.add_handler(MessageHandler(Filters.voice, voice))

dispatcher.add_handler(MessageHandler(Filters.command, unknown))

# Inline Handlers
# Handlers go brrr..

updater.start_polling()
updater.idle()
