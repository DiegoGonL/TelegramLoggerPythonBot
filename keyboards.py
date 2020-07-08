from telegram import ReplyKeyboardMarkup


def get_yes_no_keyboard():

    reply_keyboard = [
        ['Yes', 'No'],
        ['Go Back']
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def get_main_keyboard():

    reply_keyboard = [
        ['Change username'],
        ['Download Logs', 'Delete Logs'],
        ['Exit']
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
