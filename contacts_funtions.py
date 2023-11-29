"""Функции для сохранения контактов."""
import json
from time import sleep

from settings import bot


def save_user_id(user_data: dict) -> None:
    """Сохраняет ID пользователя в файл."""
    # Открываем файл contacts.json для чтения и записи
    with open('contacts/contacts.json', 'r+') as contacts:
        try:
            # Загружаем данные из файла в виде словаря
            data = json.load(contacts)
        except json.JSONDecodeError:
            # Обработка ошибки, если файл пуст
            data = {'users': []}

        # Проверяем, если user_id уже существует в файле
        users = data['users']
        if user_data in users:
            print(f'Пользователь с ID {user_data} уже существует в файле '
                  f'contacts.json')
        else:
            # Добавляем user_id в формате "user_id": user_id в список данных
            users.append(user_data)

            # Перемещаем указатель в начало файла
            contacts.seek(0)

            # Записываем обновленные данные обратно в файл
            json.dump({'users': users}, contacts, ensure_ascii=False)
            contacts.truncate()

            print(f'Пользователь с ID {user_data} успешно сохранен в '
                  f'файле contacts.json')


async def send_messages_for_contacts(message: str) -> None:
    """Отправляет сообщение по всей книге контакотов."""
    with open('contacts/contacts.json') as contacts:
        try:
            contacts_data = json.load(contacts)
        except json.JSONDecodeError:
            raise Exception('Нет контактов в файле')
        for user_id in contacts_data:
            await bot.send_message(chat_id=user_id, text=message)
            sleep(5)
