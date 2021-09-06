from telebot import types


from bot import bot


def render_yes_now_keyboard(user_id: int, question: str, prefix: str):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text="Да", callback_data=f"{prefix}_yes")
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text="Нет", callback_data=f"{prefix}_no")
    keyboard.add(key_no)
    bot.send_message(user_id, text=question, reply_markup=keyboard)


def render_initial_keyboard(user_id: int):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    register_button = types.KeyboardButton('Личные данные')
    today_todos = types.KeyboardButton("Что у нас сегодня?")
    todo_button = types.KeyboardButton('Добавить todo')
    keyboard.add(register_button, todo_button, today_todos)
    bot.send_message(user_id, "Выберите действие", reply_markup=keyboard)
