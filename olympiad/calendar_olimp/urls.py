from django.urls import path
from .views import *

app_name = 'calendar_olimp'

urlpatterns = [
    path('', olympiad_calendar_view, name='calendar'),
    path('events/', olympiad_events, name='olympiad_events'),
]
