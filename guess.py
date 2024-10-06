from random import randint

from telebot import TeleBot, types

from config import token


bot = TeleBot(token=token)
LOW = 1
HIGH = 100
bot_number = None

@bot.message_handler(commands=['start'])
def start(message):
    keyboard_markup = types.InlineKeyboardMarkup()

    button_start = types.InlineKeyboardButton(text = 'Начать', callback_data = 'start')
    keyboard_markup.add(button_start)

    bot.send_message(message.chat.id, 'Привет! Я - бот для игры "Угадай число", нажми "Играть" чтобы начать.', reply_markup=keyboard_markup)

@bot.message_handler(func=lambda message:True)
def any_other_message(message):
    bot.send_message(message.chat.id,"уйди")



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start':
        global bot_number 
        bot_number = randint(LOW, HIGH)
        output_message = f"я загадал число от {LOW} до {HIGH}. гадай"
        message = call.message 
        #bot.delete_message(chat_id=message.chat.id, message_id = message.id)
        bot.edit_message_text(chat_id=message.chat.id, message_id = message.id, text=output_message)
        bot.register_next_step_handler(message, process_guess_number_step)

def process_guess_number_step(message):
    str_number = message.text 
    if not str_number.isdigit():
        bot.send_message(message.chat.id, 'ээээ, числами пиши')
        bot.register_next_step_handler(message, process_guess_number_step)
        return 
    number = int(str_number)
    if number == bot_number:
        output_message = "крутой"
    elif number < bot_number:
        output_message = "мое число бльше"
    else:
        output_message = "мое число меньше"
    
    bot.send_message(message.chat.id, output_message)

    if output_message != 'крутой':
        bot.register_next_step_handler(message, process_guess_number_step)
bot.infinity_polling()                         