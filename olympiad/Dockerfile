# Используем официальный образ Python
FROM python:3.12
COPY . /app
# Устанавливаем рабочую директорию
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["bash", "-c", "cd olympiad && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && python -m daphne -b 0.0.0.0 -p 8000 olympiad.asgi:application "]
