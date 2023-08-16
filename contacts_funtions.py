import json
from time import sleep

from settings import bot


def save_user_id(user_id: str, full_name: str, username: str) -> None:
    # Открываем файл contacts.json для чтения и записи
    with open('contacts/contacts.json', 'r+') as contacts:
        try:
            # Загружаем данные из файла в виде словаря
            data = json.load(contacts)
        except json.JSONDecodeError:
            # Обработка ошибки, если файл пуст
            data = {}

        # Проверяем, если user_id уже существует в файле
        if user_id in data:
            print(
                f'Пользователь с ID {user_id} уже существует в файле contacts.json')
        else:
            # Добавляем user_id в формате "user_id": user_id в словарь данных
            data.update({
                user_id: {
                    'fullname': full_name,
                    'username': username
                }
            })

            # Перемещаем указатель в начало файла
            contacts.seek(0)

            # Записываем обновленные данные обратно в файл
            json.dump(data, contacts, ensure_ascii=False)
            contacts.truncate()

            print(
                f'Пользователь с ID {user_id} успешно сохранен в файле contacts.json')


async def send_messages_for_contacts(message: str) -> None:
    with open('contacts/contacts.json') as contacts:
        try:
            contacts_data = json.load(contacts)
        except json.JSONDecodeError:
            raise Exception('Нет контактов в файле')
        for user_id in contacts_data:
            await bot.send_message(chat_id=user_id, text=message)
            sleep(5)
