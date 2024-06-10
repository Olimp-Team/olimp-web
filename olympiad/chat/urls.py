from django.urls import path
from chat.views import *

app_name = 'chat'
urlpatterns = [
    path('', index, name='index'),
]
