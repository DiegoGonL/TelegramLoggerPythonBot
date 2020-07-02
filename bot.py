import logging
from config import TOKEN

from telegram.ext import CommandHandler, Updater

updater = Updater(token=TOKEN, use_context=True)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Empiezo a registrar los mensajes")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()


main()
