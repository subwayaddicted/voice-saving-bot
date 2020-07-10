from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import logging, json, mysql.connector


class VoiceSavingBot:
	def __init__(self):
		with open("config.json") as json_config:
			self.data = json.load(json_config)

		self.init_db(self.data)

		self.updater = Updater(token=self.data["telegram"]["token"], use_context=True)
		self.dispatcher = self.updater.dispatcher

		logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
							level=logging.INFO)
		self.logger = logging.getLogger(__name__)

		self.add_handlers(self.dispatcher)

	def enable(self):
		self.updater.start_polling()
		self.updater.idle()

	def add_handlers(self, dispatcher):
		dispatcher.add_handler(CommandHandler('start', self.start))
		# Message Handlers
		dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.echo))
		dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

		# dispatcher.add_handler(ConversationHandler(
		# 	entry_points=[MessageHandler(Filters.voice, self.voice)],
		#
		# 	states=[],
		#
		# 	fallbacks=[],
		# ))

	def start(self, update: Update, context: CallbackContext):
		self.logger.info("User %s %s with id: %d started bot", update.effective_user.first_name,
					update.effective_user.last_name,
					update.effective_user.id)
		context.bot.send_message(chat_id=update.effective_chat.id,
								 text="I'm a bot, please talk to me! This is testclass start func")

	def echo(self, update: Update, context: CallbackContext):
		context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

	def voice(self, update: Update, context: CallbackContext):
		voice_id = update.message.voice.file_id
		user_id = update.effective_user.id

		file = context.bot.getFile(update.message.voice.file_id)
		file_name = str(user_id) + '__' + voice_id + '.ogg'
		file_path = 'voice_messages/' + file_name

		file.download(file_path)

		update.message.reply_text('Voice saved!')

		return 0

	def command(self, update: Update, context: CallbackContext):
		void = 'foo'

	def unknown(self, update: Update, context: CallbackContext):
		self.logger.info("User %s %s with id: %d tried unknown command: " + update.message.text,
					update.effective_user.first_name,
					update.effective_user.last_name, update.effective_user.id)
		context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

	def init_db(self, data):
		self.db = mysql.connector.connect(
			host=data["mysql"]["host"],
			user=data["mysql"]["user"],
			password=data["mysql"]["password"],
			database=data["mysql"]["db"]
		)

		self.db_cursor = self.db.cursor()


bot = VoiceSavingBot()
bot.enable()
