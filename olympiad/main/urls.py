from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [

    # Страницы учеников
    path('', HomePageView.as_view(), name='home'),
    # Страницы учителей

    # Страницы администратора
    path('olympiad/list/', ListOlympiad.as_view(), name='list_olympiad'),
    path('delete/olympiad/<int:Olympiad_id>', OlympiadDelete.as_view(), name='olympiad_remove'),

]
