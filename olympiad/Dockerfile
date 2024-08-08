# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости проекта
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Выполняем миграции и запускаем сервер
CMD ["bash", "-c", " python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && python -m daphne -b 0.0.0.0 -p 8000 olympiad.asgi:application "]
