import logging
import os
from logging.handlers import RotatingFileHandler
from random import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

from bots_func import menu_buttons, get_main_menu
from constants import faq, text_message_ansers
from dictionary_functions import serch_key_by_part

load_dotenv()

logging.basicConfig(
    level=logging.ERROR,
    filename='program.log',
    filemode="a",
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    encoding="UTF-8"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("main_logs.log", encoding="UTF-8")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


async def on_start(_) -> None:
    print("The RT-Bot are started!!!")


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(TELEGRAM_TOKEN)
dispetcher = Dispatcher(bot)


@dispetcher.message_handler(commands=["start"])
async def echo_start(message: types.Message) -> None:
    logger.info(
        f'Получена команда /start от пользователя {message.from_user.username} id = {message.from_user.id}.')
    text = "Что Вас интересует?"
    logger.info(
        f'Попытка отправить сообщение: "{text}" для пользователя {message.from_user.username} id = {message.from_user.id}.')
    try:
        await message.answer(
            text=text,
            reply_markup=menu_buttons(faq)
        )
        logger.info(
            f'сообщение:"{text}" пользователя {message.from_user.username} id = {message.from_user.id} успешно отправлено.')

        await message.delete()
    except Exception as error:
        logger.exception(
            f'Что то пошло не так при работе функции echo_start ошибка: {error}')


@dispetcher.message_handler()
async def text_message_handler(message: types.Message) -> None:
    logger.info(
        f'Получено сообщение:"{message.text}", от пользователя {message.from_user.username} id = {message.from_user.id}.')
    try:
        text = choice(text_message_ansers)
        logger.info(
            f'Попытка отправить сообщение: "{text}" для пользователя {message.from_user.username} id = {message.from_user.id}..')
        await message.reply(text=text, reply_markup=get_main_menu())
        logger.info(
            f'сообщение:"{text}" пользователя {message.from_user.username} id = {message.from_user.id} успешно отправлено.')
    except Exception as error:
        logger.exception(
            f'Что то пошло не так при работе функции text_message_handler ошибка: {error}')


@dispetcher.callback_query_handler()
async def callback_key(callback: types.CallbackQuery) -> None:
    key = callback.data
    logger.info(
        f'Нажата кнопка: "{key}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
    try:
        if key == "Главное меню":
            text = "Что Вас интересует?"
            logger.info(
                f'Попытка отправить сообщение: "{text}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=text,
                reply_markup=menu_buttons(faq)
            )
            return await callback.answer()
        result = serch_key_by_part(faq, key)
        if isinstance(result, dict):
            keyboard = menu_buttons(result)
            text = "Выберете вопрос"
            message = callback.message
            logger.info(
                f'Попытка отправить сообщение: "{text}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
            await bot.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=keyboard.add(
                    InlineKeyboardButton(text="Главное меню",
                                         callback_data="Главное меню"))
            )
            await callback.answer()
        else:
            logger.info(
                f'Попытка отправить сообщение: "{result}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
            await callback.message.edit_text(text=result, reply_markup=get_main_menu(),
                                             parse_mode="HTML",
                                             disable_web_page_preview=True)
    except Exception as error:
        logger.exception(
            f'Что то пошло не так при работе функции callback_key ошибка: {error}')


if __name__ == "__main__":
    executor.start_polling(dispetcher, on_startup=on_start)
