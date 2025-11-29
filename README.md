# Coffee Shop API

RESTful API для интернет-магазина кофе на Django REST Framework.

## Особенности

- ✅ JWT аутентификация
- ✅ CRUD операции для всех моделей
- ✅ Пагинация и фильтрация
- ✅ Swagger документация
- ✅ CORS поддержка для фронтенда
- ✅ Права доступа на уровне пользователя

## Установка

1. Клонируйте репозиторий:
```bash
git clone <your-repo-url>
cd coffee_shop
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Примените миграции:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запустите сервер:
```bash
python manage.py runserver 9000
```