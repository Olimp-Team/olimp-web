from django.urls import path
from .views import InboxView, SendMessageView

urlpatterns = [
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('send/', SendMessageView.as_view(), name='send_message'),
]
