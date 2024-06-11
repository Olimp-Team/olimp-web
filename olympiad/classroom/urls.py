from django.urls import path
from .views import *

app_name = 'classroom'

urlpatterns = [

    path('tecaher/', OlympiadDelete.as_view(), name='olympiad_remove'),

    path('classroom/list/', ListClassroom.as_view(), name='list_classroom'),

]
