"""Классы для машины состояний."""
from aiogram.dispatcher.filters.state import StatesGroup, State


class MessageStatesGroup(StatesGroup):
    """Класс для приема обращения от пользователя."""

    address = State()
    name = State()
    phone = State()
    consumer_email = State()
    question = State()
    feedback = State()
    confirmation = State()
