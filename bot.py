import datetime
import telebot 
import config
import user_contact

from telebot import types 

bot = telebot.TeleBot(config.token)

contacts = []
name = None 
phone_number = None 

def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_contact_button = types.KeyboardButton('Добавить контакт')
    show_contacts_button = types.KeyboardButton('Показать все контакты')     
    keyboard.add(add_contact_button, show_contacts_button)

    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я - бот для записи контактов.", reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, handle_main_commands)

def handle_main_commands(message):
    if message.text == 'Добавить контакт':
        #print('Пользователь захотел добавить контакт')
        delete_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Как зовут нового контакта?', reply_markup=delete_keyboard)
        bot.register_next_step_handler(message, process_next_step)
    elif message.text == 'Показать все контакты':
        bot.send_message(message.chat.id, 'Список всех контактов:')
        bot.register_next_step_handler(message, handle_main_commands)
    else:
        bot.send_message(message.chat.id, 'Команда не найдена')
        bot.register_next_step_handler(message, handle_main_commands)

def process_next_step(message):
    name = message.text 

    if not name:
        bot.send_message(message.chat.id, 'Имя контакта не может быть пустым.')
        bot.register_next_step_handler(message, process_next_step)
        return

    #contact_builder.add_name(name)
    bot.send_message(message.chat.id, 'Номер телефона:')
    bot.register_next_step_handler(message, process_phone_number_step)

def process_phone_number_step(message):
    phone_number = message.text

    if not phone_number:
        bot.send_message(message.chat.id, 'Номер контакта не может быть пустым.')
        bot.register_next_step_handler(message, process_next_step)
        return

    #contact_builder.add_phone_number(phone_number)

    keyboard = types.InlineKeyboardMarkup()

    skip_button = types.InlineKeyboardButton(text='Пропустить', callback_data='skip_description')
    keyboard.add(skip_button)

    bot.send_message(message.chat.id, 'Описание:', reply_markup=keyboard)
    bot.register_next_step_handler(message, process_description_step)

def process_description_step(message):
    description = message.text

    #contact_builder.add_description(description)
    bot.send_message(message.chat.id, 'Контакт создан!', reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, handle_main_commands)





bot.infinity_polling()