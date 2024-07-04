# Используйте официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . /app/

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Применяем миграции
RUN python manage.py migrate

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Запускаем приложение с использованием Daphne
CMD ["daphne", "olympiad.asgi:application"]
