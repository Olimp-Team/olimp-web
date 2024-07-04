# chat/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
User = get_user_model()


@login_required
def chat_view(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')

    return render(request, 'chat/chat.html', {
        'other_user': other_user,
        'messages': messages
    })


@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    message.delete()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def update_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    new_content = request.POST.get('content')
    if new_content:
        message.content = new_content
        message.save()
    return JsonResponse({'status': 'ok', 'content': message.content})
