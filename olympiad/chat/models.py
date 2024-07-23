# chat/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name='school_chat')
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username} at {self.timestamp}: {self.content}"

