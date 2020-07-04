import logging
from config import TOKEN
from keyboards import main_keyboard
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram import ChatAction

updater = Updater(token=TOKEN, use_context=True)
users_dni = {}


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Buenas", reply_markup=main_keyboard)


def logger(update, context):
    if update.effective_chat.type != 'private':

        path = "logs/%s.txt" % update.effective_chat.id

        '''
        In case the folder 'logs' doesn't exists, you need to create it,
        or change the path to wherever you want to save the logs 
        '''

        try:
            f = open(path, "a")
        except FileNotFoundError:
            f = open(path, "w")

        if update.effective_user.username is None:
            update.message.reply_text(
                text=update.effective_user.first_name + ', I need you to set a username in the telegram settings'
            )
        else:

            if update.effective_user.username in users_dni:
                username = users_dni[update.effective_user.username]
            else:
                username = update.effective_user.username

            f.write("[" + update.message.date.strftime("%d/%m/%Y, %H:%M:%S") + "] " +
                    username + ": " + update.message.text + "\n")

        f.close()


def change_username(update, context):
    """
    TODO: ConversationHandler in main to be able to receive the new username as update.message.text
    """
    users_dni["%s" % update.effective_user.username] = "NewUsername"


def main():
    """
    TODO: Save the users_dni dictionary in a file, charge it at the begging and update it each time change_username is accessed
    """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    logger_handler = MessageHandler(Filters.text & (~Filters.command), logger)
    username_handler = CommandHandler('username', change_username)

    dispatcher.add_handler(username_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(logger_handler)
    updater.start_polling()
    updater.idle()


main()
