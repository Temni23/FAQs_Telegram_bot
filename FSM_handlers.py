"""Модуль с хэндлерами для приема обращения пользователя."""
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

from FSM_Classes import MessageStatesGroup, ApplicationStatesGroup
from bots_func import get_cancel, send_email, get_main_menu
from settings import bot

load_dotenv()


# Handlers для машины состояний приема обращений
async def get_address_handler(callback: types.CallbackQuery) -> None:
    """Получить адрес от пользователя."""
    await bot.send_message(chat_id=callback.from_user.id,
                           text=(
                               "Начнем! \nОтветным сообщением направляйте"
                               " мне нужную "
                               "информацию, а я ее обработаю. "
                               "\nПожалуйста, вводите "
                               "верные данные, это очень важно для "
                               "эффективного "
                               "решения Вашего вопроса.\n\n"
                               "1/6 Напишите адрес с которым связано ваше "
                               "обращение в формате \U00002757 Город, Улица,"
                               " Дом, Квартира \U00002757"),
                           reply_markup=get_cancel())
    await MessageStatesGroup.address.set()
    return await callback.answer()


async def get_name_handler(message: types.Message, state: FSMContext) -> None:
    """Получить ФИО от пользователя."""
    await message.reply(text="2/6 Напишите Вашу Фамилию Имя и Отчество",
                        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(address=message.text)


async def get_phone_handler(message: types.Message, state: FSMContext) -> None:
    """Получить телефон от пользователя."""
    await message.reply(
        text='3/6 Введите номер своего контактного телефона через "8" без '
             'пробелов, тире и прочих лишних знаков. Например "89231234567"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(name=message.text)


async def get_email_handler(message: types.Message, state: FSMContext) -> None:
    """Получить email от пользователя."""
    await message.reply(
        text='4/6 Введите номер адрес своей электронной почты. '
             'На этот адрес Вам может быть направлен ответ. '
             'Например "examle@mail.ru"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(phone=message.text)


async def get_question_handler(message: types.Message,
                               state: FSMContext) -> None:
    """Получить текст обращения от пользователя."""
    await message.reply(text="5/6 Опишите суть проблемы",
                        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(consumer_email=message.text)


async def get_feedback_handler(message: types.Message,
                               state: FSMContext) -> None:
    """Получить способ обратной связи от пользователя."""
    keyboard = get_cancel()
    button_1 = InlineKeyboardButton(text="Электронная почта",
                                    callback_data="Электронная почта")
    button_3 = InlineKeyboardButton(text="Почтой на указанный адрес",
                                    callback_data="Почтой России")
    keyboard.add(button_1).add(button_3)
    if '@' in message.from_user.mention:
        button_2 = InlineKeyboardButton(text="Сообщением в Телеграм",
                                        callback_data="Телеграм")
        keyboard.add(button_2)
    await message.reply(text="6/6 Выберете способ обратной связи "
                             "(нажмите кнопку внизу сообщения).",
                        reply_markup=keyboard)
    await MessageStatesGroup.next()
    await state.update_data(question=message.text)


async def get_conformation_handler(callback: types.CallbackQuery,
                                   state: FSMContext) -> None:
    """Получить подтверждение корректности данных от пользователя."""
    await state.update_data(feedback=callback.data)
    async with state.proxy() as data:
        address = data.get('address')
        name = data.get('name')
        question = data.get('question')
        phone = data.get('phone')
        consumer_email = data.get('consumer_email')
        feedback = data.get('feedback')
        text_checkup = (f'Готово! Давайте проверим корректность введенных '
                        f'данных.'
                        f' \nАдрес: {address}\nФИО: {name}\nТелефон: {phone}'
                        f'\nЭлектронная почта: {consumer_email}\n'
                        f'Вопрос: {question}'
                        f'\nСпособ обратной связи: {feedback}\n'
                        f'Если данные верны '
                        f'нажмите кнопку "ВСЕ ВЕРНО!"')
    keyboad = get_cancel()
    keyboad.add(InlineKeyboardButton(text='ВСЕ ВЕРНО!', callback_data='Верно'))
    await bot.send_message(chat_id=callback.from_user.id, text=text_checkup,
                           reply_markup=keyboad)
    await callback.answer()
    await MessageStatesGroup.next()


async def get_finish_handler(callback: types.CallbackQuery,
                             state: FSMContext) -> None:
    """Завершает прием обращения. Направляет его адресату."""
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Ваше обращение принято!",
                           reply_markup=get_main_menu())
    async with state.proxy() as data:
        address = data.get('address')
        name = data.get('name')
        question = data.get('question')
        phone = data.get('phone')
        consumer_email = data.get('consumer_email')
        feedback = data.get('feedback')
        user_id = callback.from_user.id
        full_name = callback.from_user.full_name
        mention = callback.from_user.mention
        text = f"""Поступило новое обращение от потребителя: {name},
        Адрес: {address},
        Телефон: {phone},
        Электронная почта: {consumer_email},
        содержание обращения: {question},
        Способ обратной связи: {feedback},
        User_id: {user_id}, Полное имя: {full_name}, Ник ТГ: {mention}"""
        await bot.send_message(chat_id=int(os.getenv('TARGET_TG')), text=text)
        await send_email(text, os.getenv('TARGET_EMAIL'))
    await callback.answer()
    await state.finish()


# Handlers для машины состояний приема заявок
async def get_application_address_handler(
        callback: types.CallbackQuery) -> None:
    """Получить адрес от пользователя."""
    await bot.send_message(chat_id=callback.from_user.id,
                           text=(
                               "Начнем! \nОтветным сообщением направляйте"
                               " мне нужную "
                               "информацию, а я ее обработаю. "
                               "\nПожалуйста, вводите "
                               "верные данные, это очень важно \U0001F64F \n\n"
                               "1/3 Напишите адрес для вывоза ТКО. "
                               "В формате Город, Улица, Дом, Квартира\n\n"
                               "\U00002757\U00002757\U00002757 ВНИМАНИЕ: Это "
                               "работает только в г. Минусинск"),
                           reply_markup=get_cancel())
    await ApplicationStatesGroup.address_application.set()
    return await callback.answer()


async def get_application_name_handler(message: types.Message,
                                       state: FSMContext) -> None:
    """Получить ФИО от пользователя."""
    await message.reply(text="2/3 Напишите Вашу Фамилию Имя и Отчество",
                        reply_markup=get_cancel())
    await ApplicationStatesGroup.next()
    await state.update_data(address_application=message.text)


async def get_application_phone_handler(message: types.Message,
                                        state: FSMContext) -> None:
    """Получить телефон от пользователя."""
    await message.reply(
        text='3/3 Введите номер своего контактного телефона \U00002757 через '
             '"8" без пробелов, тире и прочих лишних знаков\U00002757 '
             'Например "89231234567"',
        reply_markup=get_cancel())
    await ApplicationStatesGroup.next()
    await state.update_data(name_application=message.text)


async def get_application_conformation_handler(message: types.Message,
                                               state: FSMContext) -> None:
    """Получить подтверждение корректности данных от пользователя."""
    await state.update_data(phone_application=message.text)
    async with state.proxy() as data:
        address = data.get('address_application')
        name = data.get('name_application')
        phone = data.get('phone_application')
        text_checkup = (f'Готово! Давайте проверим корректность введенных '
                        f'данных.'
                        f' \nЗАЯВКА НА ВЫВОЗ ТКО.'
                        f' \nАдрес: {address}\nФИО: {name}\nТелефон: {phone}'
                        f'\nЕсли данные верны '
                        f'нажмите кнопку "ВСЕ ВЕРНО!"')
    keyboad = get_cancel()
    keyboad.add(InlineKeyboardButton(text='ВСЕ ВЕРНО!', callback_data='Верно'))
    await bot.send_message(chat_id=message.from_user.id, text=text_checkup,
                           reply_markup=keyboad)
    await ApplicationStatesGroup.next()


async def get_application_finish_handler(callback: types.CallbackQuery,
                                         state: FSMContext) -> None:
    """Завершает прием обращения. Направляет его адресату."""
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Ваша заявка принята!",
                           reply_markup=get_main_menu())
    async with state.proxy() as data:
        address = data.get('address_application')
        name = data.get('name_application')
        phone = data.get('phone_application')
        user_id = callback.from_user.id
        full_name = callback.from_user.full_name
        mention = callback.from_user.mention
        text = f"""Поступила заявка на вывоз ТКО от потребителя: {name},
        Адрес: {address},
        Телефон: {phone},
        User_id: {user_id}, Полное имя: {full_name}, Ник ТГ: {mention}"""
        await bot.send_message(chat_id=int(os.getenv('TARGET_TG')), text=text)
        await send_email(text, os.getenv('APPLICATION_TARGET_EMAIL'))
    await callback.answer()
    await state.finish()
