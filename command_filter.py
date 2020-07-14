from telegram.ext import BaseFilter


class FilterCommand(BaseFilter):
	def filter(self, message):
		command = message.text.startswith('-')

		if command is True:
			return message.text
		else:
			return False


filter_command = FilterCommand()
