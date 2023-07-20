from aiogram.dispatcher.filters.state import StatesGroup, State


class MessageStatesGroup(StatesGroup):
    address = State()
    name = State()
    phone = State()
    consumer_email = State()
    question = State()
    feedback = State()
    confirmation = State()
