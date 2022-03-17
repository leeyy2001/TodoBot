from atexit import register
from copyreg import dispatch_table
from distutils.cmd import Command
from email.message import Message
from subprocess import call
from telegram.ext import Updater
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import logging
from botAuth import BotAuth, BotMethods

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class TodoBot:
    def __init__(self, token):
        self.removeList = []
        self.todoList = []
        self.tempDict = {}

        self.TODO, self.DATE, self.LOGINPWD, self.LOGINUSER, self.REGISTERUSER = range(
            5)

        updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('help', self.help))
        dispatcher.add_handler(CommandHandler(
            'showAllTasks', self.showAllTodo))

        # Conversation handler for adding tasks.
        addTodoHandler = ConversationHandler(
            entry_points=[CommandHandler('addTask', self.startTodo)],
            states={
                self.TODO: [MessageHandler(Filters.text & (~Filters.command), self.newTodo)],
                self.DATE: [MessageHandler(
                    Filters.text & (~Filters.command), self.date)],
            },
            fallbacks=[CommandHandler('Cancel', self.cancel)]
        )

        # Conversation handler for user login.
        loginHandler = ConversationHandler(
            entry_points=[CommandHandler('login', self.login)],
            states={
                self.LOGINUSER: [MessageHandler(Filters.text & (~Filters.command), self.loginUser)],
            },
            fallbacks=[CommandHandler('Cancel', self.cancel)]
        )

        # Conversation handler for user registration
        registerHandler = ConversationHandler(
            entry_points=[CommandHandler('register', self.register)],
            states={
                self.REGISTERUSER: [MessageHandler(
                    Filters.text & (~Filters.command), self.registerUser)]
            },
            fallbacks=[CommandHandler('Cancel', self.cancel)]
        )

        dispatcher.add_handler(addTodoHandler)
        dispatcher.add_handler(loginHandler)
        dispatcher.add_handler(registerHandler)

        updater.dispatcher.add_handler(
            CommandHandler('removeTodo', self.removeTodo))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))

        updater.start_polling()

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            ''' 
        Welcome to the to-do list bot. If you are a new user, please /register as a user so that your tasks will not be sent to others. If you are a already a user /login here.
        \nEnter your task/tasks with /addTask. Look at all your tasks with /showAllTasks.\nPlease enter your information in the following format for 1 or more entries The dates should be in yyyy-dd-mm format.
        \n Type /help if you need to see what commands are available.
        ''')

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            '/register to register a new user.\n/login to login.\n/addTask to add a new task.\n/showAllTasks to all your tasks.\n/removeTodo to remove a task that you have completed.')

    def startTodo(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Please enter the task/tasks you would like to add to your todo list.")
        return self.TODO

    def newTodo(self, update: Update, context: CallbackContext):
        todo = update.message.text
        self.tempDict["task"] = todo
        update.message.reply_text(
            "When is it due? Please enter the date in the format yyyy-mm-dd or your tasks will not be saved.")
        return self.DATE

    def date(self, update: Update, context: CallbackContext):
        date = update.message.text
        self.tempDict["date"] = date
        # We add a copied version of tempDict, as we are currently using only one instance of tempDict. Thus if I change the value of tempDict, all the values in the list would change as they pointed to the same tempDict instance.
        # https://stackoverflow.com/questions/64356445/python-list-and-dictionary-being-overwritten-or-corrupted. This is the place to learn more about the issue. Remove the copy() method to see the error that results.
        BotMethods().createTask(self.token, self.tempDict.copy())
        # self.todoList.extend([self.tempDict.copy()])
        print(self.tempDict)
        update.message.reply_text(
            'If you are done press /showAllTasks to see all your todos! If you would like to add more press /addTask again!')
        return ConversationHandler.END

    def login(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Please provide your username and password in this format:\njohn john1234.\nWhere "john" is the username and "john2001" is the password.')
        return self.LOGINUSER

    def loginUser(self, update: Update, context: CallbackContext):
        loginDict = {}
        loginVal = update.message.text
        loginVal = loginVal.split(" ")
        # Create the login credentials in a json format.
        loginDict['username'] = loginVal[0]
        loginDict['password'] = loginVal[1]

        self.loginOutcome = BotAuth().login(loginDict)
        if(self.loginOutcome == 'Wrong username or password'):
            update.message.reply_text(self.loginOutcome)
        elif(self.loginOutcome != 'Wrong username or password'):
            update.message.reply_text(
                'Login successful! /showAllTasks here or /addTask here.')

        self.token = self.loginOutcome
        print(type(self.token))

        return ConversationHandler.END

    def register(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'Please provide a username and password that you would like in the format:\njohn john1234.\nWhere "john" is the username and "john1234" is the password.')

        return self.REGISTERUSER

    def registerUser(self, update: Update, context: CallbackContext):
        registerDict = {}
        registerVal = update.message.text
        registerVal = registerVal.split(" ")
        # Create the register credentials in a json format
        registerDict['username'] = registerVal[0]
        registerDict['password'] = registerVal[1]

        self.registerOutcome = BotAuth().register(registerDict)

        if(self.registerOutcome == 'User already exists'):
            update.message.reply_text(self.registerOutcome)
        elif(self.registerOutcome != 'User already exists'):
            update.message.reply_text(
                'New user created! /showAllTasks here or /addTask here.')

        self.token = self.registerOutcome
        print(self.token)

        return ConversationHandler.END

    def showAllTodo(self, update: Update, context: CallbackContext):
        update.message.reply_text("Here are all your todos!")
        # Calls the allTasks method in BotMethods which can returns a list of all tasks.
        outputList = BotMethods().allTasks(self.token)
        update.message.reply_text("".join(outputList))
        print(outputList)

    def removeTodo(self, update: Update, context: CallbackContext):
        tasksList = BotMethods().tasksOnly(self.token)

        keyboardInfo = []

        # Function to get the task in the taskList list.
        def getTask(task):
            task = task['task']
            return task

        # Putting the todos into a list
        task = map(getTask, tasksList)
        task = list(task)

        for i in task:
            # Looping through the task array to create the array for keyboard dynamically.
            keyboardInfo.extend([[InlineKeyboardButton(i, callback_data=i)]])

        keyboardInfo.extend(
            [[InlineKeyboardButton('Done', callback_data='Done')]])
        keyboard = keyboardInfo

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    def button(self, update: Update, context: CallbackContext):
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        if(query.data != 'Done'):
            self.removeList.extend([query.data])
            print(self.removeList)

        # Only once I click Done will I answer the callback query to execute the delete function.
        elif(query.data == 'Done'):
            BotMethods().removeTasks(self.token, self.removeList)

            # CallbackQueries need to be answered, even if no notification to the user is needed
            # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
            query.answer()

            # query.data contains the string that is stored in callback_data. Use print(query.data to see the value.)
            query.edit_message_text(text=f"Selected option: {self.removeList}")

    # Function to cancel the commands midway through execution
    def cancel(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            'The bot has been ended. Send /addTask to start again')
        return ConversationHandler.END
