from random import choice

from telebot import TeleBot, types

from config import token





def who_won(user_input: str, bot_input: str):
    if user_input == bot_input:
        return 'nobody'
    elif user_input == 'Камень' and bot_input == 'Ножницы' or user_input == 'Бумага' and bot_input == 'Камень' or user_input == 'Ножницы' and bot_input == 'Бумага':
        return 'user'
    else:    
        return 'bot'



def generate_bot_answer():
    choices = ['Камень','Ножницы','Бумага']
    return choice(choices)



bot = TeleBot(token=token)



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    rock_btn = types.KeyboardButton('Камень')
    scissors_btn = types.KeyboardButton('Ножницы')
    paper_btn = types.KeyboardButton('Бумага')
    markup.add(rock_btn, scissors_btn, paper_btn)

    bot.send_message(message.chat.id, "Привет. Предлагаю сыграть в камень-ножницы-бумага. Выбирай:", reply_markup=markup)

    bot.register_next_step_handler(message, game)

def game(message):
    user_input = message.text
    bot_input = generate_bot_answer()
    
    winner = who_won(user_input, bot_input)
    if winner == 'nobody':
        bot_response = 'Ничья'
    elif winner == 'user':
        bot_response = f'Поздравляют с победой! Я загадал - {bot_input}'
    else:
        bot_response = f'Ты проиграл. Я загадал - {bot_input}'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    play_again = types.KeyboardButton('/start')
    markup.add(play_again)

    bot.send_message(message.chat.id, bot_response, reply_markup = markup)



bot.infinity_polling()
