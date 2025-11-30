# Coffee Shop API

RESTful API для интернет-магазина кофе на Django REST Framework с PostgreSQL и Docker.

## Особенности

- ✅ JWT аутентификация
- ✅ CRUD операции для всех моделей
- ✅ Пагинация и фильтрация
- ✅ Swagger документация
- ✅ CORS поддержка для фронтенда
- ✅ Docker контейнеризация с PostgreSQL
- ✅ Права доступа на уровне пользователя

## 🏗️ Архитектура

### Модели данных:
- **Категории** (Categories) - группы товаров
- **Товары** (Products) - кофе и аксессуары
- **Заказы** (Orders) - заказы пользователей
- **Элементы заказа** (OrderItems) - состав заказов
- **Отзывы** (Reviews) - отзывы на товары

### Технологический стек:
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT tokens
- **Documentation**: Swagger/OpenAPI
- **Containerization**: Docker + Docker Compose

## 📦 Установка и запуск

### Предварительные требования:
- Docker Desktop
- Docker Compose

### Быстрый старт:

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/tooo196/coffee_shop_online_api.git
cd coffee_shop_online
```
2. Запустите приложение:
```bash
docker-compose up --build
```
3. Приложение будет доступно по адресам:

API: http://localhost:8001/api/
Swagger: http://localhost:8001/swagger/
Admin: http://localhost:8001/admin/

## Дополнительные команды

**Инициализация тестовых данных**
```bash
docker-compose exec web python scripts/init_data.py
```

**Создание суперпользователя**
```bash
docker-compose exec web python manage.py createsuperuser
```

**Просмотр логов**
```bash
docker-compose logs web
docker-compose logs db
```

**Остановка приложения**
```bash
docker-compose down
```

## 📚 API Endpoints
### **Аутентификация**:

- POST /api/auth/register/ - регистрация пользователя
- POST /api/auth/token/ - получение JWT токена
- POST /api/auth/token/refresh/ - обновление токена
- GET/PUT /api/auth/profile/ - профиль пользователя

### **Основные endpoints**:

- GET/POST /api/categories/ - категории товаров 
- GET/POST /api/products/ - товары
- GET/POST /api/orders/ - заказы (требует аутентификации)
- GET/POST /api/reviews/ - отзывы (требует аутентификации)

### **Особые endpoints**:

- GET /api/products/featured/ - рекомендованные товары 
- GET /api/products/{id}/reviews/ - отзывы конкретного товара

## 🔐 Аутентификация

API использует JWT аутентификацию:

1. Получение токена:
```bash
curl -X POST http://localhost:8001/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'
```

2. Использование токена в запросах:
```bash
curl -H "Authorization: Bearer <your_token>" \
  http://localhost:8001/api/orders/
```
## 🗃️ База данных
### **Структура базы данных**:
```sql
Category (1) → (N) Product (1) → (N) Review
User (1) → (N) Order (1) → (N) OrderItem (N) → (1) Product
```
### Миграции:
```bash
# Создание миграций
docker-compose exec web python manage.py makemigrations

# Применение миграций
docker-compose exec web python manage.py migrate
```

## 🐳 Docker
### **Структура контейнеров**:

- web - Django приложение
- db - PostgreSQL база данных

### **Полезные команды Docker**:
```bash
# Пересборка образов
docker-compose build --no-cache

# Запуск в фоновом режиме
docker-compose up -d

# Остановка с удалением volumes
docker-compose down -v

# Просмотр работающих контейнеров
docker-compose ps
```