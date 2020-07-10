from telegram import Update
from telegram.ext import Updater
import logging, json, mysql.connector


class Bot:
	def __init__(self):
		with open("config.json") as json_config:
			self.data = json.load(json_config)

		self.init_db(self.data)

		self.updater = Updater(token=self.data["telegram"]["token"], use_context=True)
		self.dispatcher = self.updater.dispatcher

		logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
							level=logging.INFO)
		self.logger = logging.getLogger(__name__)

	def enable(self):
		self.updater.start_polling()
		self.updater.idle()

	def init_db(self, data: dict):
		self.db = mysql.connector.connect(
			host=data["mysql"]["host"],
			user=data["mysql"]["user"],
			password=data["mysql"]["password"],
			database=data["mysql"]["db"]
		)

		self.db_cursor = self.db.cursor()

	def logger_message(self, update: Update, string: str):
		self.logger.info("User %s %s with id: %d %s", update.effective_user.first_name, update.effective_user.last_name,
						 update.effective_user.id, string)
