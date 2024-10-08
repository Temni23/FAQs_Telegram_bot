"""

В модуле собраны функция формирующие клавиатуры для работы бота.

Также функция для отправки почты.

"""

import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging.handlers import RotatingFileHandler

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("logs/main_logs.log", encoding="UTF-8")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def menu_buttons(faq: dict) -> InlineKeyboardMarkup:
    """Принимает словарь, формирует из ключей словаря кнопки.

    Возвращает Inline клавиатуру
    """
    logger.debug(
        'Пробую сформировать клавиатуру функция menu_buttons.')
    keybord = InlineKeyboardMarkup(row_width=1)
    for key in faq.keys():
        button = InlineKeyboardButton(text=key, callback_data=key[:32])
        keybord.add(button)
    logger.debug(
        f'Сформирована клавиатура {keybord}')
    return keybord


def get_main_menu() -> InlineKeyboardMarkup:
    """Формирует и возвращает Inline клавиатуру, главное меню.

    Направить обращение
    """
    application = os.getenv("APPLICATION")
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Главное меню',
                                  callback_data='Главное меню')
    button2 = InlineKeyboardButton(text='Написать обращение',
                                   callback_data='Написать обращение')
    if application:
        button3 = InlineKeyboardButton(text='Заявка на вывоз ТКО МИНУСИНСК',
                                   callback_data='Подать заявку')
        keyboard.add(button).add(button2).add(button3)
        return keyboard
    keyboard.add(button).add(button2)
    return keyboard


def get_cancel() -> InlineKeyboardMarkup:
    """Формирует и возвращает Inline клавиатуру с одной кнопкой Отмена."""
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Отмена', callback_data='cancel')
    keyboard.add(button)
    return keyboard


async def send_email(message_text, target_email):
    """Отправляет письмо на заданную почту."""
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD_EMAIL")
    time = datetime.now()

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = target_email
    msg[
        'Subject'] = (f"Новое обращение принято ботом "
                      f"{time.strftime('%Y-%m-%d %H:%M')}")
    msg.attach(MIMEText(message_text))
    try:
        mailserver = smtplib.SMTP('smtp.yandex.ru', 587)

        mailserver.ehlo()
        # Защищаем соединение с помощью шифрования tls
        mailserver.starttls()
        # Повторно идентифицируем себя как зашифрованное соединение
        # перед аутентификацией.
        mailserver.ehlo()
        mailserver.login(email, password)

        mailserver.sendmail(email, target_email, msg.as_string())

        mailserver.quit()
    except smtplib.SMTPException:
        print("Ошибка: Невозможно отправить сообщение")
