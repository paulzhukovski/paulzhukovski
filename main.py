import telebot
from telebot import types
import csv
import os
from datetime import datetime

API_TOKEN = "1928649101:AAGLtmeskhGzOyDZn3K8SKR7PeT0b9FeBRA"

bot = telebot.TeleBot(API_TOKEN)



users = {}
todo = {}


def is_valid_name_surname(name_surname):
    return not (" " in name_surname or len(name_surname) < 2)

def is_valid_text_todo(todo_text):
    return  (" " in todo_text or len(todo_text) > 1)


@bot.message_handler(content_types=['text'])
def start(message):
    user_id = message.from_user.id
    if message.text == 'Регистрация':
        users[user_id] = {}
        users[user_id]["id"] = user_id
        remove_initial_keyboard(user_id, ' Как тебя зовут?')
        bot.register_next_step_handler(message, get_name)
    elif message.text == 'todo':
        todo[user_id] = {}
        todo[user_id]["id"] = user_id
        remove_initial_keyboard(user_id, ' Введи текст задачи')
        bot.register_next_step_handler(message, get_todo)
    else:
        render_initial_keyboard(user_id)

def get_todo(message):
    todo_text = message.text
    user_id = message.from_user.id
    if is_valid_text_todo(todo_text):
        todo[user_id]["todo"] = todo_text.title()
        bot.send_message(user_id, "Введи дату в формате: день. месяц. год")
        bot.register_next_step_handler(message, get_data)
    else:
        bot.send_message(user_id, "Введите корректную задачу")
        bot.register_next_step_handler(message, get_todo)


def get_data(message):
    data = message.text
    user_id = message.from_user.id
    data = datetime.strptime(data, "%d.%m.%Y")
    if data <= datetime.now():
        bot.send_message(user_id, 'Введите реальную дату, пожалуйста')
        bot.register_next_step_handler(message, get_data)
    else:
        todo[user_id]["data"] = message.text
        todo_text = todo[user_id]["todo"]
        question = f"Задача {todo_text}. выполнить:  {message.text} ?"
        render_yes_now_keyboard(user_id, question, 'regtodo')



def get_name(message):
    user_id = message.from_user.id
    name = message.text.title()
    if is_valid_name_surname(name):
        users[user_id]["name"] = name.title()
        bot.send_message(user_id, "Какая у тебя фамилия?")
        bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(user_id, "Введите корректное имя")
        bot.register_next_step_handler(message, get_name)


def get_surname(message):
    surname = message.text
    user_id = message.from_user.id
    if is_valid_name_surname(surname):
        users[user_id]["surname"] = surname.title()
        bot.send_message(user_id, "Сколько тебе лет?")
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(user_id, "Введите корректную фамилию")
        bot.register_next_step_handler(message, get_surname)


def get_age(message):
    age_text = message.text
    user_id = message.from_user.id
    if age_text.isdigit():
        age = int(age_text)
        if not 10 <= age <= 100:
            bot.send_message(user_id, 'Введите реальный возраст, пожалуйста')
            bot.register_next_step_handler(message, get_age)
        else:
            users[user_id]['age'] = int(age)
            name = users[user_id]['name']
            surname = users[user_id]['surname']
            question = f"Тебе {age} лет и тебя зовут {name} {surname}?"
            render_yes_now_keyboard(user_id, question, 'reg')
    else:
        bot.send_message(user_id, 'Введите цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)

@bot.callback_query_handler(func=lambda call: call.data.startswith("regtodo_"))
def todo_worker(call):
    user_id = call.from_user.id
    if call.data == 'regtodo_yes':
        bot.send_message(user_id, "Спасибо, я запомню!")
        csv_dir = os.path.join("telegram_bot")
        file_path = os.path.join(csv_dir, "todo.csv")
        fieldnamestodo = ['id', 'todo', 'data']
        print(todo)

        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
            with open(file_path, 'w') as csv_file:
                w = csv.DictWriter(csv_file, fieldnames=fieldnamestodo)
                w.writeheader()
                w.writerow(todo[user_id])

        with open(file_path, 'a') as csv_file:
            w = csv.DictWriter(csv_file, fieldnames=fieldnamestodo)
            w.writerow(todo[user_id])

    elif call.data == 'regtodo_no':
        users.pop(user_id, None)
        render_initial_keyboard(user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("reg_"))
def callback_worker(call):
    user_id = call.from_user.id
    if call.data == 'reg_yes':
        bot.send_message(user_id, "Спасибо, я запомню!")
        # код вставляем сюда
        csv_dir = os.path.join("telegram_bot")
        file_path = os.path.join(csv_dir, "users.csv")
        fieldnames = ['id', 'name', 'surname', 'age']

        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
            with open(file_path, 'w') as csv_file:
                w = csv.DictWriter(csv_file, fieldnames=fieldnames)
                w.writeheader()
                w.writerow(users[user_id])

        with open(file_path, 'a') as csv_file:
            w = csv.DictWriter(csv_file, fieldnames=fieldnames)
            w.writerow(users[user_id])

    elif call.data == 'reg_no':
        users.pop(user_id, None)
        render_initial_keyboard(user_id)


def render_yes_now_keyboard(user_id: int, question: str, prefix: str):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да", callback_data=f"{prefix}_yes")
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет", callback_data=f"{prefix}_no")
    keyboard.add(key_no)
    bot.send_message(user_id, text=question, reply_markup=keyboard)


def render_initial_keyboard(user_id: int):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    register_button = types.KeyboardButton('Регистрация')
    todo_button = types.KeyboardButton('todo')
    keyboard.add(register_button, todo_button)
    bot.send_message(user_id, "Выберите действие", reply_markup=keyboard)


def remove_initial_keyboard(user_id: int, message: str):
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(user_id, message, reply_markup=keyboard)



if __name__ == '__main__':
    bot.polling(none_stop=True)