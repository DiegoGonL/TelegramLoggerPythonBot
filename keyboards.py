from telegram import ReplyKeyboardMarkup

reply_keyboard = [['Cambiar DNI'],
                  ['Cambiar Nombre de Grupo'],
                  ['Salir']]
main_keyboard = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
