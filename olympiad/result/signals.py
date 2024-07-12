# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Result
from olympiad.telegram_bot import send_result_update


@receiver(post_save, sender=Result)
def notify_result_update(sender, instance, **kwargs):
    send_result_update(instance)
