import os
from aiogram import Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from FSM_Classes import MessageStatesGroup
from FSM_handlers import *
from bots_func import get_cancel, send_email
from handlers import *

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

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dispetcher = Dispatcher(bot, storage=storage)

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


@dispetcher.message_handler(state=MessageStatesGroup.address)
async def get_name(message: types.Message, state: FSMContext) -> None:
    await get_name_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.name)
async def get_phone(message: types.Message, state: FSMContext) -> None:
    await get_phone_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.phone)
async def get_email(message: types.Message, state: FSMContext) -> None:
    await get_email_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.consumer_email)
async def get_question(message: types.Message, state: FSMContext) -> None:
    await get_question_handler(message, state)


@dispetcher.message_handler(state=MessageStatesGroup.question)
async def get_feedback(message: types.Message, state: FSMContext) -> None:
    await get_feedback_handler(message, state)


@dispetcher.callback_query_handler(state=MessageStatesGroup.feedback)
async def get_conformation(callback: types.CallbackQuery, state: FSMContext) -> None:
    await get_conformation_handler(callback, state)


@dispetcher.callback_query_handler(state=MessageStatesGroup.confirmation)
async def get_finish(callback: types.CallbackQuery, state: FSMContext) -> None:
    await get_finish_handler(callback, state)


@dispetcher.message_handler()
async def random_text_message_answer(message: types.Message) -> None:
    """Функция отправляет случайный ответ из предустановленного списка на текстовое
    сообщение пользователя"""
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
