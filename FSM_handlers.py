import os

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

from FSM_Classes import MessageStatesGroup
from bots_func import get_cancel, send_email, get_main_menu

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(TELEGRAM_TOKEN)


async def get_address_handler(callback: types.CallbackQuery) -> None:
    await bot.send_message(chat_id=callback.from_user.id,
                           text="Напишите адрес с которым связано ваше обращение",
                           reply_markup=get_cancel())
    await MessageStatesGroup.address.set()
    return await callback.answer()


async def get_name_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="Напишите ФИО", reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(address=message.text)


async def get_phone_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text='Введите номер своего контактного телефона через "8" без пробелов, '
             'тире и прочих лишних знаков. Например "89231234567"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(name=message.text)


async def get_email_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(
        text='Введите номер адрес своей электронной почты. На этот адрес Вам может быть направлен ответ. '
             'Например "examle@mail.ru"',
        reply_markup=get_cancel())
    await MessageStatesGroup.next()
    await state.update_data(phone=message.text)


async def get_question_handler(message: types.Message, state: FSMContext) -> None:
    await message.reply(text="Опишите суть проблемы", reply_markup=get_cancel())
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
    await message.reply(text="Выберете способ обратной связи", reply_markup=keyboard)
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


async def get_finish_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
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
