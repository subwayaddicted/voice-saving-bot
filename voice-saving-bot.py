from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import bot, re, os

WRONG_COMMAND, COMMAND = range(2)


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
			entry_points=[MessageHandler(Filters.voice, self.voice)],

			states={
				WRONG_COMMAND: [MessageHandler(Filters.text & Filters.command, self.wrong_command)],

				COMMAND: [MessageHandler(Filters.text & Filters.command, self.command)]
			},

			fallbacks=[CommandHandler('cancel', self.cancel)],
		))

		# Message Handlers
		dispatcher.add_handler(MessageHandler(Filters.text, self.retrieve))  # Retrieve command starting with -
		dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))  # Unknown Command

	def save(self, update: Update, context: CallbackContext):
		update.message.reply_text('Please send me voice message!')

		return None

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

		update.message.reply_text('Voice saved! Please send me a command which you want it to refer to! Just write down the word (without /?! or ~).'
								  'Or just send /cancel if you changed your mind.')

		return COMMAND

	def command(self, update: Update, context: CallbackContext):
		command = update.message.text

		check = self.is_alpha_check(update, command)

		if check is True:
			self.logger_message(update, 'set command for ' + self.voice_file_name + ' named ' + command)

			return self.insert_voice_message(update, command)

	def wrong_command(self, update: Update, context: CallbackContext):
		command = update.message.text

		check = self.is_alpha_check(update, command)

		if check is True:
			self.logger_message(update, 'set command for ' + self.voice_file_name + ' named ' + command)

			return self.insert_voice_message(update, command)

	def cancel(self, update: Update, context: CallbackContext):
		self.logger_message(update, 'cancelled voice saving conversation. File ' + self.voice_file_name + 'will be deleted.')

		update.message.reply_text("Bye! Don't be afraid, voice message is going to be deleted right now!")

		os.remove('voice_messages/' + self.voice_file_name + '.ogg')

		return ConversationHandler.END

	def retrieve(self, update: Update, context: CallbackContext):
		message = update.message.text

		# todo: regex filters
		# filtered_message = re.findall(r'\b-\w+', message)
		# self.logger_message(update, 'command filtered: ' + filtered_message[0])

		self.db_cursor.execute("SELECT filename FROM voice_messages WHERE command =%s", (message, ))

		result = self.db_cursor.fetchone()
		filename = result[0]

		if result is not None:
			self.logger_message(update, 'retrieved message ' + filename + ' with ' + message + ' command')

			file_path = 'voice_messages/' + filename + '.ogg'
			file = open(file_path, 'rb')

			context.bot.send_voice(chat_id=update.effective_chat.id, voice=file)
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

	def unknown(self, update: Update, context: CallbackContext):
		self.logger_message(update, 'tried unknown command: ' + update.message.text)

		context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

	def insert_voice_message(self, update: Update, command: str):
		sql = "INSERT INTO voice_messages (user_id, filename, command) VALUES (%s, %s, %s)"
		val = (update.effective_user.id, self.voice_file_name, '-' + command)
		self.db_cursor.execute(sql, val)
		self.db.commit()

		update.message.reply_text(
			'Voice message is saved! You can access it by sending it with "-" prefix, check it out!')

		return ConversationHandler.END

	def is_alpha_check(self, update: Update, command: str):
		check = str(command).isalpha()
		if check is False:
			self.logger_message(update, 'entered wrong command ' + command)
			update.message.reply_text(
				'Sry, your message contains something beside pure characters, please enter another one!')

			return WRONG_COMMAND
		else:
			return True


bot = VoiceSavingBot()
bot.enable()
