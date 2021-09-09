import os

DATABASE_PATH = "database"

TODO_FILE = os.path.join(DATABASE_PATH, "todo.db")

TODO_FIELDNAMES = ['user_id', 'todo_text', 'date']

DATE_FORMAT = "%d.%m.%Y"

