import logging
import os
from logging.handlers import RotatingFileHandler
from random import choice

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

from bots_func import menu_buttons, get_main_menu, get_cancel, send_email
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

storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dispetcher = Dispatcher(bot, storage=storage)


class MessageStatesGroup(StatesGroup):
    address = State()
    name = State()
    phone = State()
    consumer_email = State()
    question = State()
    feedback = State()
    confirmation = State()


@dispetcher.message_handler(commands=["start"])
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

        await message.delete()
    except Exception as error:
        logger.exception(
            f'Что то пошло не так при работе функции echo_start ошибка: {error}')


@dispetcher.callback_query_handler(lambda callback: callback.data == 'cancel',
                                   state="*")
async def cmd_cancel(callback: types.CallbackQuery, state: FSMContext) -> None:
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


@dispetcher.callback_query_handler(
    lambda callback: callback.data == "Написать обращение")
async def get_adress(callback: types.CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Напишите адрес с которым связано ваше обращение",
                           reply_markup=get_cancel())
    await MessageStatesGroup.address.set()
    return await callback.answer()


@dispetcher.message_handler(state=MessageStatesGroup.address)
async def get_name(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="Напишите ФИО", reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(address=message.text)


@dispetcher.message_handler(state=MessageStatesGroup.name)
async def get_phone(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text='Введите номер своего контактного телефона через "8" без пробелов, '
             'тире и прочих лишних знаков. Например "89231234567"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(name=message.text)


@dispetcher.message_handler(state=MessageStatesGroup.phone)
async def get_email(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text='Введите номер адрес своей электронной почты. На этот адрес Вам может быть направлен ответ. '
             'Например "examle@mail.ru"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(phone=message.text)


@dispetcher.message_handler(state=MessageStatesGroup.consumer_email)
async def get_trobble(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="Опишите суть проблемы", reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(consumer_email=message.text)


@dispetcher.message_handler(state=MessageStatesGroup.question)
async def get_feedback(message: types.Message, state: FSMContext) -> None:
    keyboard = get_cancel()
    button_1 = InlineKeyboardButton(text="Электронная почта",
                                    callback_data="Электронная почта")
    button_2 = InlineKeyboardButton(text="Сообщением в Телеграм",
                                    callback_data="Телеграм")
    button_3 = InlineKeyboardButton(text="Почтой на указанный адрес",
                                    callback_data="Почтой России")
    keyboard.add(button_1).add(button_2).add(button_3)
    await message.reply(text="Выберете способ обратной связи", reply_markup=keyboard)
    await MessageStatesGroup.next()
    await state.update_data(question=message.text)


@dispetcher.callback_query_handler(state=MessageStatesGroup.feedback)
async def get_conformation(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(feedback=callback.data)
    async with state.proxy() as data:
        address = data.get('address')
        name = data.get('name')
        question = data.get('question')
        phone = data.get('phone')
        consumer_email = data.get('consumer_email')
        feedback = data.get('feedback')
        # text = f"Поступило новвое обращение от потребителя: {name}, " \
        #        f"\n указавшего адрес: {address}, " \
        #        f"\n содержание обращения: {question}"
        # await bot.send_message(chat_id=287530282, text=text)
        # await send_email(text)
        text_checkup = f'Давайте проверим корректность введенных данных.' \
                       f' \nАдрес: {address}\nФИО: {name}\nТелефон: {phone}' \
                       f'\nЭлектронная почта: {consumer_email}\nВопрос: {question}' \
                       f'\nСпособ обратной связи: {feedback}'
    keyboad = get_cancel()
    keyboad.add(InlineKeyboardButton(text='ВСЕ ВЕРНО!', callback_data='Верно'))
    await bot.send_message(chat_id=callback.from_user.id, text=text_checkup,
                           reply_markup=keyboad)
    await callback.answer()
    await MessageStatesGroup.next()


@dispetcher.callback_query_handler(state=MessageStatesGroup.confirmation)
async def get_conformation(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.send_message(chat_id=callback.from_user.id, text="Обращение принято!",
                           reply_markup=get_main_menu())
    async with state.proxy() as data:
        address = data.get('address')
        name = data.get('name')
        question = data.get('question')
        phone = data.get('phone')
        consumer_email = data.get('consumer_email')
        feedback = data.get('feedback')
        text = f"Поступило новое обращение от потребителя: {name}, " \
               f"\nАдрес: {address}\nТелефон: {phone}" \
               f"\nЭлектронная почта: {consumer_email}" \
               f"\nсодержание обращения: {question}\nСпособ обратной связи: {feedback}"
        await bot.send_message(chat_id=int(os.getenv('TARGET_TG')), text=text)
        await send_email(text)
    await callback.answer()
    await state.finish()


@dispetcher.message_handler()
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


@dispetcher.callback_query_handler()
async def faq_callback_key(callback: types.CallbackQuery) -> None:
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


if __name__ == "__main__":
    executor.start_polling(dispetcher, on_startup=on_start, skip_updates=True)
