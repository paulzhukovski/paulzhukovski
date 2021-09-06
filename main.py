import os

from telebot import types

from bl.add_todo import process_add_todo
from bl.common import render_initial_keyboard
from bl.get_todos import process_today_todos
from bl.registrations import start_registrations
from bot import bot

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")


@bot.message_handler(content_types=['text'])
def start(message):
    user_id = message.from_user.id
    if message.text == 'Личные данные':
        start_registrations(user_id, message)
    elif message.text == 'Добавить todo':
        process_add_todo(user_id, message)
    elif message.text == "Что у нас сегодня?":
        process_today_todos(user_id)
    else:
        render_initial_keyboard(user_id)


def remove_initial_keyboard(user_id: int, message: str):
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(user_id, message, reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
