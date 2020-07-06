from telegram import ReplyKeyboardMarkup


def get_yes_no_keyboard():

    reply_keyboard = [
        ['Si', 'No'],
        ['Salir']
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def get_main_keyboard():

    reply_keyboard = [
        ['Cambiar username'],
        ['Descargar Logs', 'Borrar Logs'],
        ['Salir']
    ]
    return ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
