## Проект «API для Yatube»
Проекь разработки API для социальной сети **Yatube**. Написание API согласно документации, представленно в http://127.0.0.1:8000/redoc/.

В проекте использована библиотека **Django REST Framework**, используемая для улучшения работы с **REST API**

В процессе разработки проекта познакомился и поработал с форматом **JSON**, с _Сериализаторами_, с **JWT** 

В проекте использованы: `Python 3.9, Django 4.0.6, SQLite, etc.`

### Инструкция по запуску
- Склонируйте проект `git clone https://github.com/Andrey-Kugubaev/api_final_yatube.git`
- установите и активируйте виртуальное окружение `python -m venv venv (или python3 -m venv venv)` `source venv/Scripts/activate (или source venv/bin/activate)`
- установите зависимости `pip install -r requirements.txt`
- создайте файл _.env_, где пропишите ключ для _settings.py_
- создайте базу данных и выполните миграции `python manage.py makemigrations` `python manage.py migrate`
- запустите сервер `python manage.py runserver`
- 