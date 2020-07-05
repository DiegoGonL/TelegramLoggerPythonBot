import logging

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler

from config import TOKEN
from keyboards import main_keyboard

updater = Updater(token=TOKEN, use_context=True)
users_dni = {}
MAIN, SETTINGS = range(2)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome, please check the settings")


def ajustes(update, context):
    print("Entro en ajustes")
    update.message.reply_text(
        text=update.effective_user.first_name + ", ¿QUE QUIERES HACER?",
        reply_markup=main_keyboard)

    return MAIN


def logger(update, context):
    if update.effective_chat.type == 'private':

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


def ret_settings(update, context):
    print("Entro en retSettings")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Write the new username",
        reply_markup=main_keyboard)
    return SETTINGS


def change_username(update, context):
    users_dni["%s" % update.effective_user.username] = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your new username has been saved as %s" % update.message.text,
        reply_markup=main_keyboard)
    return MAIN


def exit_conv(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Salgo de la conver")
    return ConversationHandler.END


if __name__ == '__main__':
    """
    TODO: Save the users_dni dictionary in a file, charge it at the begging and update it each time change_username is accessed
    """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dispatcher = updater.dispatcher
    logger_handler = MessageHandler(Filters.text & (~Filters.command), logger)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN: [MessageHandler(Filters.regex('Cambiar DNI'), ret_settings),
                   MessageHandler(Filters.regex('^(Cambiar Nombre de Grupo)$'), ret_settings)],

            SETTINGS: [MessageHandler(Filters.text, change_username)]
        },

        fallbacks=[MessageHandler(Filters.regex('^(Salir)$'), exit_conv)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(logger_handler)
    updater.start_polling()
    updater.idle()
