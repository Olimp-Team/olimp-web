from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('<str:username>/', chat_view, name='chat'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('update_message/<int:message_id>/', update_message, name='update_message'),
]

