"""Содержит функции для работы со словарем ответов."""

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("logs/main_logs.log", encoding="UTF-8")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def serch_key_by_part(dictionary: dict, part: str) -> str or dict:
    """Ищет в словаре значение по первым 32 символам ключа.

    32 символа связаны с ограничением callback_data в InlineButton
    """
    logger.debug(
        f'Пробую найти ответ на запрос {part} функция serch_key_by_part')
    for key in dictionary.keys():
        if part == key[:32]:
            logger.debug(
                f'Возвращаю ответ {dictionary[key]} на запрос {part}'
                f'функция serch_key_by_part')
            return dictionary[key]
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = serch_key_by_part(value, part)
            if result is not None:
                logger.debug(
                    f'Возвращаю ответ {result} на запрос {part}'
                    f'функция serch_key_by_part')
                return result
