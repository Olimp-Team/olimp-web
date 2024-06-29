from django.shortcuts import render
from django.http import JsonResponse
from main.models import Olympiad


def olympiad_calendar_view(request):
    return render(request, 'calendar/calendar.html')


def olympiad_events(request):
    olympiads = Olympiad.objects.all()
    events = []
    for olympiad in olympiads:
        event = {
            'title': olympiad.name,
            'start': olympiad.date.strftime('%Y-%m-%d') + 'T' + olympiad.time.strftime('%H:%M:%S'),
            'description': olympiad.description,
            'location': olympiad.location,
        }
        events.append(event)
    return JsonResponse(events, safe=False)
