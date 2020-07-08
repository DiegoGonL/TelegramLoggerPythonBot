import logging
import os
import keyboards
import json

from telegram import ReplyKeyboardRemove, TelegramError
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler
from config import config

dict_usernames = None
updater = Updater(token=config.TOKEN, use_context=True)
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

        # In case the log file doesn't exists, it will be created
        try:
            f = open(path, "a")
        except FileNotFoundError:
            f = open(path, "w")

        if (update.effective_user.username is None) & (str(update.effective_user.id) not in dict_usernames):
            context.bot.send_message(
                chat_id=update.effective_user.id,
                text=update.effective_user.first_name +
                ", you don't have neither a telegram username, nor a username set in this bot"
                " so i will use your user id. Please, set an username in the Telegram settings"
                " or using /start and selecting change username, otherwise"
            )

            username = str(update.effective_user.id)

        elif update.effective_user.username in dict_usernames:
            username = dict_usernames[update.effective_user.username]

        elif str(update.effective_user.id) in dict_usernames:
            username = dict_usernames[str(update.effective_user.id)]

        else:
            username = update.effective_user.username

        f.write("[" + update.message.date.strftime("%d/%m/%Y, %H:%M:%S") + "] " +
                username + ": " + update.message.text + "\n")

        f.close()


def bot_description(update, context):

    try:
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Here you have a short description of what this bot can do:\n\n"
                 "Use /start to access the full functionality of this bot.\n"
                 "None of the answers to the bot will be saved in the logs, neither the bot messages\n\n"
                 "- If you add me to a group chat, I will register the messages that are sent to that group, never private conversations like this one\n\n"
                 "- You can change the name that will be reflected in the logs\n\n"
                 "- You can ask me to send your log file with any file name that you give me\n\n"
                 "- You can delete your logs any time (THIS ACTION CANT BE UNDONE)")

    except TelegramError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please start the private conversation with me.",
            reply_to_message_id=update.message.message_id
        )


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
        text="Are you sure you want to remove the logs, THIS ACTION CANT BE UNDONE",
        reply_markup=keyboards.get_yes_no_keyboard()
    )

    return REMOVE_LOGS


def change_username(update, context):
    dict_usernames["%s" % str(update.effective_user.id)] = update.message.text

    with open(config.USERNAME_FILE, 'w') as file:
        json.dump(dict_usernames, file, sort_keys=True, indent=4)

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

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your logs have been removed",
            reply_markup=keyboards.get_main_keyboard()
        )

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


def set_handlers(dispatcher):
    logger_handler = MessageHandler(Filters.text & (~Filters.command), logger)

    help_handler = CommandHandler('help', bot_description)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MAIN: [MessageHandler(Filters.regex('Change username'), return_change_username),
                   MessageHandler(Filters.regex('Download Logs'), return_download_logs),
                   MessageHandler(Filters.regex('Delete Logs'), return_remove_logs)],

            CHANGE_USERNAME: [MessageHandler(Filters.text & (~Filters.command), change_username)],

            DOWNLOAD_LOGS: [MessageHandler(Filters.text & (~Filters.command), download_logs)],

            REMOVE_LOGS: [MessageHandler(Filters.regex('^(Yes)$') & (~Filters.command), remove_logs),
                          MessageHandler(Filters.regex('^(Go Back|No)$') & (~Filters.command), return_main)]
        },

        fallbacks=[MessageHandler(Filters.regex('^(Exit)$'), exit_conv)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(logger_handler)


if __name__ == '__main__':
    """
    TODO: Language Selector and user info buttons 
    """
    try:
        os.mkdir(config.LOGS_FOLDER)
    except FileExistsError:
        pass

    try:
        with open(config.USERNAME_FILE, 'r') as dictionary:
            if os.stat(config.USERNAME_FILE).st_size == 0:
                dict_usernames = {}
            else:
                dict_usernames = json.load(dictionary)

    except FileNotFoundError:
        with open(config.USERNAME_FILE, 'w') as dictionary:
            pass
        dict_usernames = {}

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dp = updater.dispatcher
    set_handlers(dispatcher=dp)

    updater.start_polling()
    updater.idle()
