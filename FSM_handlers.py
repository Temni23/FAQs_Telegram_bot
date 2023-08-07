import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

from FSM_Classes import MessageStatesGroup
from bots_func import get_cancel, send_email, get_main_menu
from settings import bot

load_dotenv()


async def get_address_handler(callback: types.CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id,
                           text=("Начнем! \nОтветным сообщением направляйте мне нужную "
                                 "информацию, а я ее обработаю. \nПожалуйста, вводите "
                                 "верные данные, это очень важно для эффективного "
                                 "решения Вашего вопроса.\n\n"
                                 "1/6 Напишите адрес с которым связано ваше обращение"),
                           reply_markup=get_cancel())
    await MessageStatesGroup.address.set()
    return await callback.answer()


async def get_name_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="2/6 Напишите Вашу Фамилию Имя и Отчество",
                        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(address=message.text)


async def get_phone_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text='3/6 Введите номер своего контактного телефона через "8" без пробелов, '
             'тире и прочих лишних знаков. Например "89231234567"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(name=message.text)


async def get_email_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text='4/6 Введите номер адрес своей электронной почты. '
             'На этот адрес Вам может быть направлен ответ. '
             'Например "examle@mail.ru"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(phone=message.text)


async def get_question_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="5/6 Опишите суть проблемы", reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(consumer_email=message.text)


async def get_feedback_handler(message: types.Message, state: FSMContext) -> None:
    keyboard = get_cancel()
    button_1 = InlineKeyboardButton(text="Электронная почта",
                                    callback_data="Электронная почта")
    button_2 = InlineKeyboardButton(text="Сообщением в Телеграм",
                                    callback_data="Телеграм")
    button_3 = InlineKeyboardButton(text="Почтой на указанный адрес",
                                    callback_data="Почтой России")
    keyboard.add(button_1).add(button_2).add(button_3)
    await message.reply(text="6/6 Выберете способ обратной связи "
                             "(нажмите кнопку внизу сообщения).",
                        reply_markup=keyboard)
    await MessageStatesGroup.next()
    await state.update_data(question=message.text)


async def get_conformation_handler(callback: types.CallbackQuery,
                                   state: FSMContext) -> None:
    await state.update_data(feedback=callback.data)
    async with state.proxy() as data:
        address = data.get('address')
        name = data.get('name')
        question = data.get('question')
        phone = data.get('phone')
        consumer_email = data.get('consumer_email')
        feedback = data.get('feedback')
        text_checkup = f'Готово! Давайте проверим корректность введенных данных.' \
                       f' \nАдрес: {address}\nФИО: {name}\nТелефон: {phone}' \
                       f'\nЭлектронная почта: {consumer_email}\nВопрос: {question}' \
                       f'\nСпособ обратной связи: {feedback}\nЕсли данные верны ' \
                       f'нажмите кнопку "ВСЕ ВЕРНО!"'
    keyboad = get_cancel()
    keyboad.add(InlineKeyboardButton(text='ВСЕ ВЕРНО!', callback_data='Верно'))
    await bot.send_message(chat_id=callback.from_user.id, text=text_checkup,
                           reply_markup=keyboad)
    await callback.answer()
    await MessageStatesGroup.next()


async def get_finish_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.send_message(chat_id=callback.from_user.id, text="Ваше обращение принято!",
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
        await send_email(text)
    await callback.answer()
    await state.finish()
