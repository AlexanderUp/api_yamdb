# Сверхинновационное приложение api_yamdb

Сверхнновационное приложение, социальная сеть для любителей творчества, позволяющее создавать рецензии на художественные произведения и ставлять комментарии на них.

## Запуск приложения:

- Клонируем репозиторий:

```git clone https://github.com/AlexanderUp/api_yamdb.git``
    
- Переходим в папку проекта:

```cd api_yamdb```

- Настраиваем виртуальное окружение:

```python3 -m pip venv venv```

- Активируем виртуальное окружение:

```source venv/bin/activate```

- Устанавливаем зависимости:

```python3 -m pip install -r requirements.txt```

- Переходим в папку проекта:

```cd api_yamdb```

- Создаем и применяем миграции БД:

```python3 manage.py makemigrations```

```python3 manage.py migrate```

- Создаем суперпользователя, следуем инструкциям из терминала:

```python3 manage.py createsuperuser```

- Запускаем отладочный сервер:

```python3 manage.py runserver```

## Примеры запросов

Документация API доступна по адресу:

```127.0.0.1:8000/redoc/```

## Использованные технологии

Django REST Framework 3.12.4