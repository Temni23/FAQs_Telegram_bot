import logging
from logging.handlers import RotatingFileHandler
from random import choice

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton

from bots_func import menu_buttons, get_main_menu
from constants import faq, text_message_ansers
from contacts_funtions import save_user_id
from dictionary_functions import serch_key_by_part
from settings import bot

logging.basicConfig(
    level=logging.ERROR,
    filename='logs/program.log',
    filemode="a",
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    encoding="UTF-8"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("logs/main_logs.log", encoding="UTF-8")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


async def command_start(message: types.Message) -> None:
    """Функция обрабатывает команду start"""
    logger.info(
        f'Получена команда /start от пользователя {message.from_user.username} id = {message.from_user.id}.')
    text = "Здравствуйте! Выберете категорию вопроса."
    logger.info(
        f'Попытка отправить сообщение: "{text}" для пользователя {message.from_user.username} id = {message.from_user.id}.')
    try:
        await message.answer(
            text=text,
            reply_markup=menu_buttons(faq)
        )
        logger.info(
            f'сообщение:"{text}" пользователя {message.from_user.username} id = {message.from_user.id} успешно отправлено.')
        save_user_id(str(message.from_user.id),
                     message.from_user.full_name, message.from_user.username)

        await message.delete()
    except Exception as error:
        logger.exception(
            f'Что то пошло не так при работе функции echo_start ошибка: {error}')


async def handler_cancel(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(chat_id=callback.from_user.id,
                               text="Сейчас нечего отменять, попробуйте использовать "
                                    "главное меню!",
                               reply_markup=get_main_menu())

        return await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Создание обращения прервано",
                           reply_markup=get_main_menu())
    await state.finish()
    return await callback.answer()


async def random_text_message_handler(message: types.Message) -> None:
    """Функция отправляет случайный ответ из предустановленного списка на текстовое
    сообщение пользователя"""
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


async def faq_callback_key_handler(callback: types.CallbackQuery) -> None:
    """Функция отвечает за работу с инлайн клавиатурой.
    По нажатой кнопке приходит поиск категории либо писк ответа,
    который направляется пользователю"""
    key = callback.data
    logger.info(
        f'Нажата кнопка: "{key}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
    try:
        if key == "Главное меню":
            text = "Что Вас интересует?"
            logger.info(
                f'Попытка отправить сообщение: "{text}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
            await callback.message.edit_text(text=text, reply_markup=menu_buttons(faq))
            return await callback.answer()
        result = serch_key_by_part(faq, key)  # Поиск в словаре результата по
        # нажатой пользователем кнопке
        if isinstance(result, dict):  # Если результатом поиска является словарь,
            # формируется новое меню из кнопок, где для текста кнопок используются
            # ключи словаря result
            keyboard = menu_buttons(result)
            message = callback.message
            logger.info(
                f'Попытка отправить сообщение с новой клавиатурой для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
            await bot.edit_message_reply_markup(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=keyboard.add(
                    InlineKeyboardButton(text="Главное меню",
                                         callback_data="Главное меню"))
            )
            await callback.answer()
        else:  # В окончании result содержит строковое значение которое
            # направляется пользователю в ответе
            logger.info(
                f'Попытка отправить сообщение: "{result}" для пользователя {callback.from_user.username} id = {callback.from_user.id}.')
            await callback.message.edit_text(text=result, reply_markup=get_main_menu(),
                                             parse_mode="HTML",
                                             disable_web_page_preview=True)
    except Exception as error:
        logger.exception(
            f'Что то пошло не так при работе функции callback_key ошибка: {error}')
