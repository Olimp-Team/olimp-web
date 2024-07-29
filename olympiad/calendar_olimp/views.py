from django.shortcuts import render
from django.http import JsonResponse
from main.models import Olympiad
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class OlympiadCalendarView(LoginRequiredMixin, View):
    """Страница отображения календаря олимпиад для всех пользователей"""

    def get(self, request):
        return render(request, 'calendar/calendar.html')


class OlympiadEvents(LoginRequiredMixin, View):
    """JSON response для заполнения дат и времени олимпиад"""

    def get(self, request):
        olympiads = Olympiad.objects.filter(school=request.user.school)
        events = [
            {
                'title': olympiad.name,
                'start': olympiad.date.strftime('%Y-%m-%dT%H:%M:%S'),
                'description': olympiad.description,
                'location': olympiad.location,
            }
            for olympiad in olympiads
        ]
        return JsonResponse(events, safe=False)
