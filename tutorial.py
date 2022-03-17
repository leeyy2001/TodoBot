from datetime import datetime
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging

todoList = [
    {
        "todo": "Laundry",
        "date": "19/05/2022",
    },
    {
        "todo": "Chicken",
        "date": "22/05/2022"
    }
]

outputList = []

for i in todoList:
    outputList.extend([list(i.values())[0] + " " + list(i.values())[1] + "\n"])

print(outputList)

TODO, DATE = range(2)

updater = Updater(
    token="5142577591:AAEgvNM9V7fQs7_QG-4aU4Gs3Z3ClE5kme0", use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="This bot will be your todo list manager.\nEnter a new task with /addTask.\nSee all of your tasks with /showAllTasks")


def addTask(update: Update, context: CallbackContext):
    todo = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="The task has been added to your todo list")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="When is it due?")
    date = update.message.text
    print(todo, date)
    # todoList.extend([{"todo": todo, "date": date}])
    # todoList.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))
    print(todoList)


# This loooks like "/caps hello" outputs "HELLO"
def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def showAllTasks(update: Update, context: CallbackContext):

    context.bot.send_message(
        chat_id=update.effective_chat.id, text="".join(outputList))


showTasks_handler = CommandHandler('showAllTasks', showAllTasks)
caps_handler = CommandHandler('caps', caps)
echo_handler = MessageHandler(Filters.text & (~Filters.command), addTask)
start_handler = CommandHandler('start', start)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(showTasks_handler)

updater.start_polling()
