import os

DATABASE_PATH = "database"

TODO_FILE = os.path.join(DATABASE_PATH, "todo.csv")

TODO_FIELDNAMES = ['user_id', 'todo_text', 'date']

DATE_FORMAT = "%d.%m.%Y"

USERS_FILE = os.path.join(DATABASE_PATH, "users.csv")

USERS_FIELDNAMES = ['id', 'name', 'surname', 'age']
