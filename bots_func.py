import logging
from logging.handlers import RotatingFileHandler

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("main_logs.log", encoding="UTF-8")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def menu_buttons(faq: dict) -> InlineKeyboardMarkup:
    """Принимает словарь, формирует из ключей словаря кнопки, возвращает
    Inline клавиатуру"""
    logger.debug(
        f'Пробую сформировать клавиатуру функция menu_buttons.')
    keybord = InlineKeyboardMarkup(row_width=1)
    for key in faq.keys():
        button = InlineKeyboardButton(text=key, callback_data=key[:32])
        keybord.add(button)
    logger.debug(
        f'Сформирована клавиатура {keybord}')
    return keybord


def get_main_menu() -> InlineKeyboardMarkup:
    """Формирует и возвращает Inline клавиатуру с одной кнопкой Главное меню"""
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Главное меню', callback_data='Главное меню')
    keyboard.add(button)
    return keyboard
