

# def check_tokens():
#     """Проверяет наличие токенов и данных о чате."""
#     if TELEGRAM_TOKEN is None:
#         logger.critical('Отсутствует TELEGRAM_TOKEN, проверьте файл .env')
#         raise Exception('Отсутствует TELEGRAM_TOKEN, проверьте файл .env')
#     # Комменария для Ревьювера: Вы писали про логи в данной функции
#     # "Тут не нужно логирование, так-как оно произойдет при обработке
#     # исключения в main()." Однако, при после того как я убрал логирование
#     # в данной функции перестал проходить pytest
#     # AssertionError: Убедитесь, что при отсутствии обязательных переменных
#     # окружения событие логируется с уровнем `CRITICAL`.
#     # В итоге оставил исходный вариант
#     if PRACTICUM_TOKEN is None:
#         logger.critical('Отсутствует PRACTICUM_TOKEN, проверьте файл .env')
#         raise Exception('Отсутствует PRACTICUM_TOKEN, проверьте файл .env')
#     if TELEGRAM_CHAT_ID is None:
#         logger.critical('Отсутствует TELEGRAM_CHAT_ID, проверьте файл .env')
#         raise Exception('Отсутствует TELEGRAM_CHAT_ID, проверьте файл .env')
#     return True
