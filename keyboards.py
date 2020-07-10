from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def get_yes_no_keyboard():

    reply_keyboard = [
        [InlineKeyboardButton('Yes', callback_data='Yes'), InlineKeyboardButton('No', callback_data='No')],
        [InlineKeyboardButton('Go Back', callback_data='Go Back')]
    ]
    return InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def get_main_keyboard():

    reply_keyboard = [
        [InlineKeyboardButton('Change username', callback_data='Change username')],
        [InlineKeyboardButton('Download Logs', callback_data='Download Logs'), InlineKeyboardButton('Delete Logs', callback_data='Delete Logs')],
        [InlineKeyboardButton('Exit', callback_data='Exit')]
    ]
    return InlineKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
