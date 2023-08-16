import logging
from logging.handlers import RotatingFileHandler

from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

from FSM_Classes import MessageStatesGroup
from FSM_handlers import (get_address_handler, get_name_handler,
                          get_phone_handler,
                          get_email_handler, get_question_handler,
                          get_feedback_handler,
                          get_conformation_handler, get_finish_handler)
from bots_func import get_cancel
from handlers import (command_start, handler_cancel,
                      random_text_message_handler,
                      faq_callback_key_handler)
from settings import dispetcher

load_dotenv()

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

MessageStatesGroup()


@dispetcher.message_handler(commands=["start"])
async def start_command_handler(message: types.Message):
    await command_start(message)


@dispetcher.callback_query_handler(lambda callback: callback.data == 'cancel',
                                   state="*")
async def cmd_cancel(callback: types.CallbackQuery, state: FSMContext) -> None:
    await handler_cancel(callback, state)


@dispetcher.callback_query_handler(
    lambda callback: callback.data == "Написать обращение")
async def get_address(callback: types.CallbackQuery) -> None:
    await get_address_handler(callback)


@dispetcher.message_handler(lambda message: len(message.text) < 4,
                            state=MessageStatesGroup.address)
async def check_address(message: types.Message) -> None:
    """Проверяет адрес введенный пользователем на количество символов"""
    await message.answer(
        "Введите правильный адрес. Это чрезвычайно важно для корректной "
        "работы с Вашим вопросом.",
        reply_markup=get_cancel())


@dispetcher.message_handler(state=MessageStatesGroup.address)
async def get_name(message: types.Message, state: FSMContext) -> None:
    """Функция отрабатывает если пользователь ввел валидный адрес"""
    await get_name_handler(message, state)


@dispetcher.message_handler(
    regexp=r'^[а-яА-ЯёЁa-zA-Z]+[ .-а-яА-ЯёЁa-zA-Z]+?[ -юа-яА-ЯёЁa-zA-Z]+$',
    state=MessageStatesGroup.name)
async def get_phone(message: types.Message, state: FSMContext) -> None:
    """Функция отрабатывает если пользователь ввел валидные ФИО"""
    await get_phone_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.name)
async def check_name(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        "Представьтесь пожалуется, отправьте ответным сообщением Ваше ФИО."
        "Например: Иванов Петр Иванович",
        reply_markup=get_cancel())


@dispetcher.message_handler(
    regexp=r'^(8|\+7)[\- ]?\(?\d{3}\)?[\- ]?\d{3}[\- ]?\d{2}[\- ]?\d{2}$',
    state=MessageStatesGroup.phone)
async def get_email(message: types.Message, state: FSMContext) -> None:
    """Функция отрабатывает если пользователь ввел валидный телефон"""
    await get_email_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.phone)
async def check_phone(message: types.Message) -> None:
    """Проверяет номер телефона введенный пользователем, функция отрабатывает
    если введено что-то не соответсвующее паттерну из get_email"""
    await message.answer(
        "Введите корректный номер телефона без пробелов и тире."
        "Например: 89081234567",
        reply_markup=get_cancel())


@dispetcher.message_handler(
    regexp=r'^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,7}$',
    state=MessageStatesGroup.consumer_email)
async def get_question(message: types.Message, state: FSMContext) -> None:
    """Функция отрабатывает если пользователь ввел валидный email"""
    await get_question_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.consumer_email)
async def check_email(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите корректный адрес электронной почты.",
                         reply_markup=get_cancel())


@dispetcher.message_handler(lambda message: len(message.text) < 5,
                            state=MessageStatesGroup.question)
async def check_question(message: types.Message) -> None:
    """Проверяет вопрос введенный пользователем на количество символов"""
    await message.answer(
        "Опишите свой вопрос хотя бы в двух словах, пожалуйста.",
        reply_markup=get_cancel())


@dispetcher.message_handler(state=MessageStatesGroup.question)
async def get_feedback(message: types.Message, state: FSMContext) -> None:
    await get_feedback_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.feedback)
async def check_conformation(message: types.Message) -> None:
    """Функция отрабатывает если пользователь ввел ответ на сообщение
     с инлайн клавиатурой"""
    await message.answer("Воспользуйтесь клавиатурой в предыдущем сообщении.",
                         reply_markup=get_cancel())


@dispetcher.message_handler(state=MessageStatesGroup.confirmation)
async def check_finish(message: types.Message) -> None:
    """Функция отрабатывает если пользователь ввел ответ на сообщение
         с инлайн клавиатурой"""
    await message.answer("Воспользуйтесь клавиатурой в предыдущем сообщении.",
                         reply_markup=get_cancel())


@dispetcher.callback_query_handler(state=MessageStatesGroup.feedback)
async def get_conformation(callback: types.CallbackQuery,
                           state: FSMContext) -> None:
    await get_conformation_handler(callback, state)


@dispetcher.callback_query_handler(state=MessageStatesGroup.confirmation)
async def get_finish(callback: types.CallbackQuery, state: FSMContext) -> None:
    await get_finish_handler(callback, state)


@dispetcher.message_handler()
async def random_text_message_answer(message: types.Message) -> None:
    """Функция отправляет случайный ответ из предустановленного списка на
    текстовое сообщение пользователя"""
    await random_text_message_handler(message)


@dispetcher.callback_query_handler()
async def faq_callback_key(callback: types.CallbackQuery) -> None:
    """Функция отвечает за работу с инлайн клавиатурой.
    По нажатой кнопке приходит поиск категории либо писк ответа,
    который направляется пользователю"""
    await faq_callback_key_handler(callback)


if __name__ == "__main__":
    # if not check_tokens():
    #     sys.exit()
    executor.start_polling(dispetcher, skip_updates=True)
