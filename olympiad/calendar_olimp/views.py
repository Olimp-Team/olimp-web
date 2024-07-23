from django.shortcuts import render
from django.http import JsonResponse
from main.models import Olympiad
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class OlympiadCalendarView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'calendar/calendar.html')


class OlympiadEvents(LoginRequiredMixin, View):
    def get(self, request):
        olympiads = Olympiad.objects.filter(school=request.user.school)
        events = [
            {
                'title': olympiad.name,
                'start': f"{olympiad.date.strftime('%Y-%m-%d')}T{olympiad.time.strftime('%H:%M:%S')}",
                'description': olympiad.description,
                'location': olympiad.location,
            }
            for olympiad in olympiads
        ]
        return JsonResponse(events, safe=False)
