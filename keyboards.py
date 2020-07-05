from telegram import ReplyKeyboardMarkup

reply_keyboard = [['Cambiar username'],
                  ['Descargar logs'],
                  ['Salir']]
main_keyboard = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
