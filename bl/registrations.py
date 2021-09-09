from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from bl.common import render_yes_now_keyboard, render_initial_keyboard
from bot import bot


USERS = {}
Base = declarative_base()

engine = create_engine(
    "sqlite+pysqlite:///database/users.db",
    echo=True,
    future=True
)
Session = sessionmaker(engine)

class Customer(Base):
    __tablename__ = "customer"

    user_id = Column(Integer,  primary_key=True)
    id_telegram = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    age = Column(Integer, nullable=False)


    def __str__(self):
        return f"Customer <id_telegram:{self.id_telegram}, name:{self.name}, surname:{self.surname}, age:{self.age}>"

Base.metadata.create_all(engine)


def is_valid_name_surname(name_surname):
    return not (" " in name_surname or len(name_surname) < 2)


def start_registrations(user_id, message):
    USERS[user_id] = {}
    bot.send_message(user_id, ' Как тебя зовут?')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text.title()
    if is_valid_name_surname(name):
        USERS[user_id]["name"] = name.title()
        bot.send_message(user_id, "Какая у тебя фамилия?")
        bot.register_next_step_handler(message, get_surname)
    else:
        bot.send_message(user_id, "Введите корректное имя")
        bot.register_next_step_handler(message, get_name)


def get_surname(message):
    surname = message.text.title()
    user_id = message.from_user.id
    if is_valid_name_surname(surname):
        USERS[user_id]["surname"] = surname.title()
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
            USERS[user_id]['age'] = int(age)
            name = USERS[user_id]['name']
            surname = USERS[user_id]['surname']
            question = f"Тебе {age} лет и тебя зовут {name} {surname}?"
            render_yes_now_keyboard(user_id, question, 'reg')
    else:
        bot.send_message(user_id, 'Введите цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)

def reg_callback(call):
    return call.data.startswith('reg_')


@bot.callback_query_handler(func=reg_callback)
def reg_worker(call):
    user_id = call.from_user.id
    if call.data == 'reg_yes':
        bot.send_message(user_id, "Спасибо, я запомню!")
        print(USERS)
        id_tel = user_id
        name = USERS[user_id]['name']
        surname = USERS[user_id]['surname']
        age = USERS[user_id]['age']
        session = Session()
        add_id = Customer(id_telegram=id_tel, name=name,surname=surname, age=age)
        session.add(add_id)
        session.commit()

        """
        db_table_val(id=id, name=name, surname=surname, age=age)
        is_first_user = not os.path.exists(USERS_FILE)
        with open(USERS_FILE, "a") as users_csv:
            writer = csv.DictWriter(users_csv, fieldnames=USERS_FIELDNAMES)
            users_dict = USERS[user_id]
            users_dict['id'] = user_id
            if is_first_user:
                writer.writeheader()
            writer.writerow(users_dict)
             """
    elif call.data == 'reg_no':
        render_initial_keyboard(user_id)
    USERS.pop(user_id, None)

