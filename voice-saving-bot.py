from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import bot

VOICE, COMMAND = range(2)


class VoiceSavingBot(bot.Bot):
	def __init__(self):
		super().__init__()

		self.voice_file_name = None
		self.add_handlers(self.dispatcher)

	def add_handlers(self, dispatcher):
		# Command Handlers
		dispatcher.add_handler(CommandHandler('start', self.start))

		# Conversation Handlers
		dispatcher.add_handler(ConversationHandler(
			entry_points=[CommandHandler('save', self.save)],

			states={
				VOICE: [MessageHandler(Filters.voice, self.voice)],

				COMMAND: [MessageHandler(Filters.text, self.command)]
			},

			fallbacks=[CommandHandler('cancel', self.cancel)],
		))

		# Unknown Command Handler
		dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

	def save(self, update: Update, context: CallbackContext):
		update.message.reply_text('Please send me voice message!')

		return VOICE

	def start(self, update: Update, context: CallbackContext):
		self.logger.info("User %s %s with id: %d started bot", update.effective_user.first_name,
						 update.effective_user.last_name,
						 update.effective_user.id)
		context.bot.send_message(chat_id=update.effective_chat.id,
								 text="I'm a bot, please talk to me!")

	def voice(self, update: Update, context: CallbackContext):
		voice_id = update.message.voice.file_id
		user_id = update.effective_user.id

		file = context.bot.getFile(update.message.voice.file_id)
		self.voice_file_name = str(user_id) + '__' + voice_id
		file_name = self.voice_file_name + '.ogg'
		file_path = 'voice_messages/' + file_name
		file.download(file_path)

		self.logger_message(update, 'sent voice stored as ' + file_name)

		update.message.reply_text('Voice saved! Please send me a command/codename which you want it to refer to! Or '
								  'just send /cancel if you changed your mind.')

		return COMMAND

	def command(self, update: Update, context: CallbackContext):
		command = update.message.text

		self.logger_message(update, 'set command for ' + self.voice_file_name + ' named ' + command)

		update.message.reply_text(
			'Voice message is saved! You can access it by sending it with "-" prefix, check it out!')

		# todo: SQL save info about voice

		return ConversationHandler.END

	def cancel(self, update: Update, context: CallbackContext):
		self.logger_message(update, 'cancelled voice saving conversation. File ' + self.voice_file_name + 'will be deleted.')

		update.message.reply_text("Bye! Don't be afraid, voice message is going to be deleted right now!")

		# todo: SQL delete info about voice

		return ConversationHandler.END

	def unknown(self, update: Update, context: CallbackContext):
		self.logger_message(update, 'tried unknown command: ' + update.message.text)

		context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


bot = VoiceSavingBot()
bot.enable()
