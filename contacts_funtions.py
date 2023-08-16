import json


def save_user_id(user_id: str, full_name: str, username: str) -> None:
    # Открываем файл contacts.json для чтения
    with open('contacts/contacts.json', 'r') as contacts:
        try:
            # Загружаем данные из файла в виде словаря
            data = json.load(contacts)
        except json.JSONDecodeError:
            # Обработка ошибки, если файл пуст
            data = {}

    # Проверяем, если user_id уже существует в файле
    if user_id in data:
        print(f'Пользователь с ID {user_id} уже существует в файле contacts.json')
    else:
        # Добавляем user_id в формате "user_id": user_id в словарь данных
        data[user_id] = [full_name, username]

        # Открываем файл contacts.json для записи
        with open('contacts/contacts.json', 'w') as contacts:
            # Записываем обновленные данные обратно в файл
            json.dump(data, contacts, ensure_ascii=False)

        print(f'Пользователь с ID {user_id} успешно сохранен в файле contacts.json')