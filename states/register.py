from telebot.states import State, StatesGroup


class Register(StatesGroup):
    fio = State()
    age = State()
    course = State()
    contact = State()
    address = State()
    study_time = State()
    document = State()
    confirmation = State()
