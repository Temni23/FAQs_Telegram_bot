# FAQs_Telegram_bot

Этот бот может отвечать на предустановленные вопросы по выбору пользователя. Также бот принимает обращения от пользователей и пересылает их в почту и ТГ выбранному лицу. Бот может сохранять контакты пользователей. Ведет логирование.

## Описание:

Проект FAQs_Telegram_bot выполнен Климовым А.В. распространится в
ознакомительных целях. Коммерческое использование возможно только с согласия
автора.

Контакт автора temni23@yandex.ru

## Установка на windows:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Temni23/FAQs_Telegram_bot.git
```

```
cd FAQs_Telegram_bot
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Работа с проектом

Создайте файл .env В этом файле добавьте переменную TELEGRAM_TOKEN в которую
стоокой сохраните токен вашего бота

Также создайте в этом файле переменные присвоив им СВОИ значения

```
EMAIL=django-your_text   #Используется для входа в почту с которой пересылается обращение пользователя
PASSWORD_EMAIL=your_text #Используется для входа в почту с которой пересылается обращение пользователя
TARGET_EMAIL=your_text   #Используется для отправки обращения пользователя на указанную почту
TARGET_TG=your_text  #Используется для отправки обращения пользователя в телеграмм ответственному лицу
APPLICATION=False  #Для формирования заявок в клавиатуре главного меню, по умолчанию False
```

## Работа со словарем

Создайте файл constants.py в папке constants

В файле constants.py создайте переменную faq в нее добавьте словарь. Ключ -
вопрос для поиска, значение - ответ. В качестве значения может использоваться
вложенный словарь. Вложенные словари стоит использовать для структурирования
вопросов по категориям.

Пример словаря 
```
faq = {"Категория 1": {"Вопрос 1.1.": "ответ на вопрос 1.1"}}
```

Затем, запустите код в файле main.py

# Работа с ботом через Докер

Бот может быть запущен с использованием Docker

Скопируйте файл docker-compose.yml на сервер с установленным docker и docker compose

Создайте файл constants.py в папке с файлом docker-compose.yml

В файле constants.py создайте переменную faq в нее добавьте словарь. Ключ -
вопрос для поиска, значение - ответ. В качестве значения может использоваться
вложенный словарь. Вложенные словари стоит использовать для структурирования
вопросов по категориям.

Пример словаря 
```
faq = {"Категория 1": {"Вопрос 1.1.": "ответ на вопрос 1.1"}}
```

Создайте файл .env в одном каталоге с файлом docker-compose.yml. В этом файле 
добавьте переменную TELEGRAM_TOKEN в которую
стоокой сохраните токен вашего бота

Также создайте в этом файле переменные присвоив им СВОИ значения

```
EMAIL=django-your_text   #Используется для входа в почту с которой пересылается обращение пользователя
PASSWORD_EMAIL=your_text #Используется для входа в почту с которой пересылается обращение пользователя
TARGET_EMAIL=your_text   #Используется для отправки обращения пользователя на указанную почту
TARGET_TG=your_text  #Используется для отправки обращения пользователя в телеграмм ответственному лицу

Выполните команду

```
sudo docker compose up
```

Бот запустится в Docker контейнере.

Логи бота будут сохранены в volume logs
Контакты в volume contacts
