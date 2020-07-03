from telegram import ReplyKeyboardMarkup

reply_keyboard = [['Cambiar Nombre de Grupo'],
                  ['Cambiar DNI'],
                  ['Salir']]
main_keyboard = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
