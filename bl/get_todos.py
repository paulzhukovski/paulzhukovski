import csv
import os
import datetime

from bl.constants import TODO_FIELDNAMES, TODO_FILE, DATE_FORMAT
from bot import bot


def process_today_todos(user_id):
    if not os.path.exists(TODO_FILE):
        bot.send_message(user_id, "Для вас нет задач на сегодня")
    else:
        todos = get_todays_todos(user_id)
        bot.send_message(user_id, todos)


def get_todays_todos(user_id):
    user_todos = []
    today = datetime.datetime.now().date()
    with open(TODO_FILE) as todos_file:
        reader = csv.DictReader(todos_file, fieldnames=TODO_FIELDNAMES)
        for row in reader:
            if not row["user_id"] == str(user_id):
                continue
            todo_date = datetime.datetime.strptime(row["date"], DATE_FORMAT).date()
            if todo_date == today:
                user_todos.append(row["todo_text"])
    if not user_todos:
        message = "Для вас нет задач на сегодня"
    else:
        enumerate_todos = []
        for index, todo in enumerate(user_todos, start=1):
            enumerate_todos.append(f"{index}. {todo};")
        greeting = "Зравствуйте, ваши задачи на сегодня:\n"
        todos = "\n".join(enumerate_todos)
        message = f"{greeting}{todos}"
    return message
