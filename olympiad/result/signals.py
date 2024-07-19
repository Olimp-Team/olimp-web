# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from result.models import Result
# from result.telegram_bot import send_result_update
#
#
# @receiver(post_save, sender=Result)
# def notify_result_update(sender, instance, **kwargs):
#     import asyncio
#     loop = asyncio.get_event_loop()
#     loop.create_task(send_result_update(instance))
