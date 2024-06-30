from datetime import datetime, timedelta

from schedule.models import Calendar, Event
from main.models import *
# Создаем календарь, если его еще нет
calendar, created = Calendar.objects.get_or_create(name='Olympiads Calendar')

# Создаем событие для каждой олимпиады
olympiads = Olympiad.objects.all()
for olympiad in olympiads:
    event = Event.objects.create(
        title=olympiad.name,
        start=datetime.combine(olympiad.date, olympiad.time),
        end=datetime.combine(olympiad.date, olympiad.time) + timedelta(hours=2),  # примерное время окончания
        calendar=calendar,
        description=olympiad.description,
        location=olympiad.location,
    )
