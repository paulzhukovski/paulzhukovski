
import os
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bl.add_todo import Todo_add
from bl.constants import TODO_FIELDNAMES, TODO_FILE, DATE_FORMAT
from bot import bot


def process_today_todos(user_id):
    if not os.path.exists(TODO_FILE):
        bot.send_message(user_id, "Для вас нет задач на сегодня")
    else:
        todos = get_todays_todos(user_id)
        bot.send_message(user_id, todos)


engine = create_engine(
    "sqlite+pysqlite:///database/todo.db",
    echo=True,
    future=True
)
Session = sessionmaker(engine)



def get_todays_todos(user_id):
    user_todos = []
    today = datetime.datetime.now().date()

    session = Session()
    for customer, text, date in session.query(Todo_add.id_telegram, Todo_add.todo_text, Todo_add.date):
        if customer == str(user_id):
            continue
        date_users = datetime.datetime.strptime(date, DATE_FORMAT).date()
        if date_users == today:
            user_todos.append(text)

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

    """"
    user_todos = []
    today = datetime.datetime.now().date()
    with Session() as session:
        add_todo = session.query(todo).filter(
            todo.email == "j.bond@mi6.uk"
        )
    
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
        """

