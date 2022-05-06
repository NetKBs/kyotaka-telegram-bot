
from telegram.ext.updater import Updater # contain API key
from telegram.update import Update # to invoke everytime a bot recieves an update (i.e. a msg)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler # to handle any normal msgs from usr
from telegram.ext.commandhandler import CommandHandler # to handle commands from the user
from telegram.ext.filters import Filters # to filter normal text, commands, img, etc
from telegram.ext import PicklePersistence # to add persistence data

from data_manager import search, add
from _token import tokenGet # where to get the token
import logging

# Erros handler to connections of getting back data
# BadConnection, NotData, BadHost

class App():
	def __init__(self):
		persistence = PicklePersistence('./models/db')
		self.updater = Updater(tokenGet(), use_context=True, persistence=persistence)

		# utilities
		self.job_checker = False # where the job is going to be saved

		# start bot, commands
		self.dispatchers()
		self.updater.start_polling()
		self.updater.idle()


	def start(self, update: Update, context: CallbackContext):
		""" Welcome """
		update.message.reply_text("Welcome.\n I'll notify you when a new chapter of your registered stories is uploaded")
		return self.help(update, context)

	def help(self, update: Update, context: CallbackContext):
		""" info, commands, hosts"""

		update.message.reply_text("Hosts (webpages from you could add stories and track its):\n1 => manganato.com (English)\n2 => lectormanga.com (Spanish)\n")

		update.message.reply_text("Commands Avaibles:\n/start => welcome\n/help => this message\n/search <name> | <host> => to find the direct links of the stories\n/add <direct-link> | <host> => use direct link to track a story\n/remove <direct-link> => remove a story added\n/show => stories added\n/track_start => start to track the stories you have added\n/track_stop => stop the track of yours stories")


	def search(self, update: Update, context: CallbackContext):
		""" Search for a story """
		try:
			sentence = ""

			# check the args, in this case the arg[0] should be the name and arg[1] the host
			# we identify this better with | here we are just making a string with the args  
			if len(context.args)-1 > 0:
				for word in context.args:
					sentence = sentence + word + " "
			else:
				sentence = context.args[0]

			# verify if there is the host option 
			if sentence.find("|") == -1: 
				raise IndexError 

			sentence = sentence.split("|") 
			name = sentence[0].strip()
			host = sentence[1].strip()

			data = search(name, host)

			if data == "BadHost":
				update.message.reply_text("Invalid host.\nTry /help")

			elif data == "BadConnection": 
				update.message.reply_text("Error with the connection")

			elif data == "NotData": 
				update.message.reply_text("Nothing found.")

			else:
				# show results
				for element in data:
					update.message.reply_text(f"Direct link to copy: {element}\n")

		except (IndexError, ValueError):
			update.message.reply_text("Usage: /search <name> | host\n\nExample: /search baki | manganato.com\n\nTo see the hosts try /help")


	# ------------------- Data handlers ------------------------

	def parse_db(self, context: CallbackContext): 
			""" For persistence data"""
			return context.user_data.setdefault('user_stories', {})

	def	add(self, update: Update, context: CallbackContext):
		""" Add series """
		try:
			sentence = ""

			# check the args, in this case the arg[0] should be the name and arg[1] the host
			# we identify this better with | here we are just making a string with the args  
			if len(context.args)-1 > 0:
				for word in context.args:
					sentence = sentence + word + " "

			# verify if there is the host option 
			if sentence.find("|") == -1: 
				raise IndexError 

			sentence = sentence.split('|')
			link = sentence[0].strip()
			host = sentence[1].strip()

			data = add(link, host)	

			if data == "BadConnection": 
				update.message.reply_text("An error had ocurred. Maybe invalid direct link or bad connection.")

			elif data == "BadHost":
				update.message.reply_text("Invalid host.\nTry /help")

			else:
				if "stories" in self.parse_db(context):

					# check if the story is added already
					for element in self.parse_db(context)["stories"]:
						if element["link"] == data["link"]:
							update.message.reply_text("Sorry, but this story has been added already!")
							return

					self.parse_db(context)["stories"].append(data) 
				else:
					# when its empty, we add the data in a list
					self.parse_db(context)["stories"] = [data] 

				update.message.reply_text("Story added")
				update.message.reply_text("To start the tracker use /track_start")

		except (IndexError, ValueError):
			update.message.reply_text("Usage: /add <direct-link> | <host>\n\nExample:/add https://manganato.com/manga-ql952046 | manganato.com\n\nTo see the hosts try /help")


	def show(self, update: Update, context: CallbackContext):
		""" Show stories added """

		if "stories" in self.parse_db(context):
			if self.parse_db(context)["stories"]: # not empty

				for story in self.parse_db(context)["stories"]:
					update.message.reply_text(f"Direct link: {story['link']}\nCurrent Chapter: {story['chapter']}")

			else:
				update.message.reply_text("There is not stories to show.\nTry /add")
		else:
			update.message.reply_text("There is not stories to show.\nTry /add")	


	def remove(self, update: Update, context: CallbackContext):
		""" Remove a story added """

		try:
			# args[0] should be the link
			link = context.args[0].lstrip()

			if "stories" in self.parse_db(context):
				if self.parse_db(context)["stories"]:

					for story in self.parse_db(context)["stories"]:
						if story["link"] == link:
							# delete story
							self.parse_db(context)["stories"].remove(story)
							update.message.reply_text("Story removed")	

				else:
					update.message.reply_text("That direct link isn't added. To check try /show")
			else:
				update.message.reply_text("That direct link isn't added. To check try /show")	

		except (IndexError, ValueError):
			update.message.reply_text("Usage: /remove <direct-link>")

	
			
	# ---------------------- Notify and tracking handler -----------------------------------
	
	def startCheckManager(self, update: Update, context: CallbackContext):
			""" Add a job to the queue """

			if "stories" in self.parse_db(context): # exist the stories dict
				if self.parse_db(context)["stories"]: # not empty

					chat_id = update.message.chat_id	
					# ------------------ IMPORTANT ---------------------
					# Because of the issue between persistent data and JobQueue when using
					# The same context params, I decided that when you create a job
					# automatically to create a global variable for checkChapterChanges exclusively
					# ------------------ ######## ---------------------
					self.context_for_job_issues = context

					if not self.job_checker: # just if there isn't a job already
						# with this we create a job. It'll call the checkCheckManager each minute
						self.job_checker = context.job_queue.run_repeating(
							self.checkChapterChanges,
							interval=60,
							first=10,
							context=chat_id)
						update.message.reply_text("Tracker started!")

					else:
						update.message.reply_text("Your are actually tracking now.\nWanna stop with /track_stop ?")
				else:
					update.message.reply_text("At least add something to track!\nTry /add")
			else:	
				update.message.reply_text("At least add something to track!\nTry /add")


	def stopCheckManager(self, update: Update, context: CallbackContext):
			""" Stop a job """	

			if self.job_checker: # there is a job
				self.job_checker.schedule_removal() # remove it
				self.job_checker = False

				update.message.reply_text("The tracker was stoped")
			else:
				update.message.reply_text("The tracker is not active.\nTry /track_start")


	def checkChapterChanges(self, context: CallbackContext):
		"""  Check if there are new chapters """

		job = context.job
		for index in range(len(self.parse_db(self.context_for_job_issues)["stories"])): 
			link = self.parse_db(self.context_for_job_issues)["stories"][index]["link"] 
			host = self.parse_db(self.context_for_job_issues)["stories"][index]["host"]
			# last chapter registered
			prev_chapter = self.parse_db(self.context_for_job_issues)["stories"][index]["chapter"]

			data = add(link, host) # reconnect with each story
			chapter = data["chapter"] # new chapter received

			# there is a new chapter
			if prev_chapter != chapter: 
				# update chapter
				self.parse_db(self.context_for_job_issues)["stories"][index]["chapter"] = chapter
				context.bot.send_message(job.context,
					text=f"New chapter\n{link}\nPrevious: {prev_chapter}\nActual: {chapter}")
	


	def text(self, update: Update, context: CallbackContext):
		""" Free text"""
		update.message.reply_text("I don't understand that command.\nTry /help")


	def dispatchers(self):
		""" Commands handler """

		self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self.updater.dispatcher.add_handler(CommandHandler('help', self.help))

		# Manage data commands --------------
		self.updater.dispatcher.add_handler(CommandHandler('search', self.search))
		self.updater.dispatcher.add_handler(CommandHandler('add', self.add))
		self.updater.dispatcher.add_handler(CommandHandler('remove', self.remove))
		self.updater.dispatcher.add_handler(CommandHandler('show', self.show))

		# Trackers commands --------------
		self.updater.dispatcher.add_handler(CommandHandler('track_start', self.startCheckManager))
		self.updater.dispatcher.add_handler(CommandHandler('track_stop', self.stopCheckManager))

		# Unkown massages and commands ---------------
		self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.text))

# Debugging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if  __name__ == "__main__":
	app = App()