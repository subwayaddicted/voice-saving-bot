from telegram.ext import Updater, CommandHandler, MessageHandler, InlineQueryHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging

updater = Updater(token='968628814:AAEyjjPinThWqec11sikYgNzvoxo6JZu3PU', use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)


# Functions
def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text='Eat this')#text=update.message.text)


def caps(update, context):
	text_caps = ' '.join(context.args).upper()
	context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def inline_caps(update, context):
	query = update.inline_query.query
	if not query:
		return
	results = list()
	results.append(
		InlineQueryResultArticle(
			id=query.upper(),
			title='Caps',
			input_message_content=InputTextMessageContent(query.upper())
		)
	)
	context.bot.answer_inline_query(update.inline_query.id, results)


# Commands handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# Message Handlers
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Inline Handlers
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

updater.start_polling()
