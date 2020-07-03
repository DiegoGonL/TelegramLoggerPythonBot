import logging
from config import TOKEN

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

updater = Updater(token=TOKEN, use_context=True)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Buenas")


def logger(update, context):

    try:
        f = open("../test.txt", "a")
    except FileNotFoundError:
        f = open("../test.txt", "w")

    if update.effective_user.username is None:
        update.message.reply_text(
            text=update.effective_user.first_name + ', necesitio que establezcas un nombre de usuario en telegram'
        )
    else:
        f.write("[" + update.message.date.strftime("%d/%m/%Y, %H:%M:%S") + "] " +
                update.effective_user.username + ": " + update.message.text + "\n")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    logger_handler = MessageHandler(Filters.text & (~Filters.command), logger)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(logger_handler)
    updater.start_polling()
    updater.idle()


main()
