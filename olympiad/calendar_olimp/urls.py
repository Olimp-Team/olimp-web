from django.urls import path
from .views import *

app_name = 'calendar_olimp'

urlpatterns = [
    path('', OlympiadCalendarView.as_view(), name='calendar'),
    path('events/', OlympiadEvents.as_view(), name='olympiad_events'),
]
