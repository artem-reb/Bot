import datetime

import telebot 

import config

import user_contact

bot = telebot.TeleBot(config.token)

contacts = []
name = None 
phone_number = None 



@bot.message_handler(commands=["start"])
def handle_message(message):
    bot.send_message(message.chat.id, "Привет! Я - бот для записи контактов.")

@bot.message_handler(commands=["current_time", 'time'])
def current_time(message):
    now = datetime.datetime.now()
    output_message = f'{now.year} год, сентябрь, {now.day} число'
    bot.send_message(message.chat.id, output_message)

@bot.message_handler(commands=["new_contact", "add"])
def new_contact(message):
    user_message = bot.reply_to(message, 'Как зовут нового контакта?')
    print(user_message.text)
    bot.register_next_step_handler(user_message, process_name_step)




def process_name_step(user_message):
    global name 
    name = user_message.text
    user_message = bot.reply_to(user_message, 'Какой номер телефона у контакта?')
    bot.register_next_step_handler(user_message, process_phone_number_step)

def process_phone_number_step(user_message):
    global phone_number
    phone_number = user_message.text

    user = user_contact.UserContact(name, phone_number)
    contacts.append(user)

    bot.send_message(user_message.chat.id, 'Вы ввели контакт.')

@bot.message_handler(commands=['contacts'])
def list_contacts(message):
    if len(contacts) == 0:
        output_message = 'У вас пока-что нет контактов.'
    else:
        for contact in contacts:
            bot.send_message(message.chat.id, str(contact))

bot.infinity_polling()