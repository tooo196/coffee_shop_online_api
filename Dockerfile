# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Создаем папку для статических файлов
RUN mkdir -p /app/staticfiles /app/media

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["gunicorn", "coffee_shop_online.wsgi:application", "--bind", "0.0.0.0:8000"]