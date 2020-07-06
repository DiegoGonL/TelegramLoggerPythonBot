import logging
import os
import keyboards

from telegram import ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler
from config import config


updater = Updater(token=config.TOKEN, use_context=True)
users_dni = {}
MAIN, CHANGE_USERNAME, DOWNLOAD_LOGS, REMOVE_LOGS = range(4)


def start(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome, please check the settings",
        reply_markup=keyboards.get_main_keyboard())

    return MAIN


def logger(update, context):

    if update.effective_chat.type != 'private':

        path = config.LOGS_FOLDER + "%s.txt" % update.effective_chat.id

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


def return_main(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="What do you want to do?",
        reply_markup=keyboards.get_main_keyboard()
    )

    return MAIN


def return_change_username(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Write the new username",
        reply_markup=ReplyKeyboardRemove()
    )

    return CHANGE_USERNAME


def return_download_logs(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Write the name for your log file",
        reply_markup=ReplyKeyboardRemove()
    )

    return DOWNLOAD_LOGS


def return_remove_logs(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Are you sure you want to remove the logs, this action cant be undone",
        reply_markup=keyboards.get_yes_no_keyboard()
    )

    return REMOVE_LOGS


def change_username(update, context):

    users_dni["%s" % update.effective_user.username] = update.message.text
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your new username has been saved as %s" % update.message.text,
        reply_markup=keyboards.get_main_keyboard()
    )

    return MAIN


def download_logs(update, context):

    try:
        context.bot.sendDocument(
            chat_id=update.effective_chat.id,
            document=open('logs/%s.txt' % update.effective_chat.id, 'rb'),
            filename='%s.txt' % update.message.text,
            reply_markup=keyboards.get_main_keyboard()
        )

    except FileNotFoundError:

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your logs are empty",
            reply_markup=keyboards.get_main_keyboard()
        )

    return MAIN


def remove_logs(update, context):

    try:
        os.remove(config.LOGS_FOLDER + "%s.txt" % update.effective_chat.id)

    except FileNotFoundError:

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your logs are empty",
            reply_markup=keyboards.get_main_keyboard()
        )

    return MAIN


def exit_conv(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="See you next time!",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


if __name__ == '__main__':
    '''
    TODO: Save the users_dni dictionary in a file, charge it at the begging and update it each time change_username is accessed
    '''

    try:
        os.mkdir(config.LOGS_FOLDER)
    except FileExistsError:
        pass

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    dispatcher = updater.dispatcher
    logger_handler = MessageHandler(Filters.text & (~Filters.command), logger)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN: [MessageHandler(Filters.regex('Cambiar username'), return_change_username),
                   MessageHandler(Filters.regex('Descargar Logs'), return_download_logs),
                   MessageHandler(Filters.regex('Borrar Logs'), return_remove_logs)],

            CHANGE_USERNAME: [MessageHandler(Filters.text & (~Filters.command), change_username)],

            DOWNLOAD_LOGS: [MessageHandler(Filters.text & (~Filters.command), download_logs)],

            REMOVE_LOGS: [MessageHandler(Filters.regex('^(Si|No)$') & (~Filters.command), remove_logs),
                          MessageHandler(Filters.regex('Salir') & (~Filters.command), return_main)]
        },

        fallbacks=[MessageHandler(Filters.regex('^(Salir)$'), exit_conv)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(logger_handler)
    updater.start_polling()
    updater.idle()
