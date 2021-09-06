import datetime
import sqlite3

from bl.common import render_yes_now_keyboard, render_initial_keyboard
from bl.constants import DATE_FORMAT
from bot import bot

TODO = {}
conn = sqlite3.connect('database/todo.db', check_same_thread=False)
cursor = conn.cursor()
"""
command =
    CREATE TABLE IF NOT EXISTS "todo"(
        id INTEGER PRIMARY KEY,
        todo VARCHAR(255),
        date VARCHAR(255)
    );
cursor.execute(command)
"""



def db_table_val(id: int, todo: str, date: str):
	cursor.execute('INSERT INTO todo (id, todo, date) VALUES (?, ?, ?)', (id, todo, date))
	conn.commit()


def process_add_todo(user_id, message):
    TODO[user_id] = {'user_id': user_id}
    bot.send_message(user_id, ' Введи текст задачи')
    bot.register_next_step_handler(message, get_todo_text)


def get_todo_text(message):
    user_id = message.from_user.id
    TODO[user_id]['todo_text'] = message.text
    bot.send_message(user_id, "Введи дату в формате: день. месяц. год")
    bot.register_next_step_handler(message, get_data)


def get_data(message):
    user_id = message.from_user.id
    try:
        date = datetime.datetime.strptime(message.text, DATE_FORMAT).date()
    except ValueError:
        bot.send_message(user_id, 'Введите дату в формате дд.мм.гггг')
        bot.register_next_step_handler(message, get_data)
    else:
        now = datetime.datetime.now().date()
        if now > date:
            bot.send_message(user_id, "Введи дату в будущем")
            bot.register_next_step_handler(message, get_data)
        else:
            TODO[user_id]["date"] = message.text
            todo = TODO[user_id]["todo_text"]
            question = (
                f"Вы назначили {message.text} слудующую "
                f"задачу: \n\n '{todo}'\n\n Подтвердить?"
            )
            render_yes_now_keyboard(user_id, question, "todo")


def todo_callback(call):
    return call.data.startswith("todo_")


@bot.callback_query_handler(func=todo_callback)
def todo_worker(call):
    user_id = call.from_user.id
    if call.data == "todo_yes":
        bot.send_message(user_id, 'Спасибо, я запомнил!')
        id = user_id
        todo = TODO[user_id]["todo_text"]
        date = TODO[user_id]["date"]
        db_table_val(id=id, todo=todo, date=date)

        """
        is_first_todo = not os.path.exists(TODO_FILE)
        with open(TODO_FILE, "a") as todos_csv:
            writer = csv.DictWriter(todos_csv, fieldnames=TODO_FIELDNAMES)
            todo_dict = TODO[user_id]
            if is_first_todo:
                writer.writeheader()
            writer.writerow(todo_dict)
        """
    elif call.data == 'todo_no':
        render_initial_keyboard(user_id)
    TODO.pop(user_id, None)
