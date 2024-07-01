from django.urls import path
from .views import *

app_name = 'calendar_olimp'

urlpatterns = [
    path('', olympiad_calendar_view.as_view(), name='calendar'),
    path('events/', olympiad_events.as_view(), name='olympiad_events'),
]
