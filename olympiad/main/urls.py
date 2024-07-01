from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [

    # Страницы учеников
    path('', HomePageView.as_view(), name='home'),
    # Страницы учителей

    # Страницы администратора
    path('olympiad/list/', OlympiadListView.as_view(), name='list_olympiad'),
    path('olympiad/new/', OlympiadCreateView.as_view(), name='olympiad_create'),
    path('olympiad/edit/<int:pk>/', OlympiadUpdateView.as_view(), name='olympiad_update'),
    path('olympiad/delete/<int:pk>/', OlympiadDeleteView.as_view(), name='olympiad_delete'),

]
