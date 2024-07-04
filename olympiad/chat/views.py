# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Q, Max, F
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from friendship.models import Friend, FriendshipRequest

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


@login_required
def chat_list_view(request):
    current_user = request.user
    # Получить список друзей текущего пользователя
    friends = Friend.objects.friends(current_user)

    # Получить последние сообщения для каждого друга
    last_messages = (
        Message.objects
        .filter(
            (Q(sender=current_user) & Q(recipient__in=friends)) |
            (Q(recipient=current_user) & Q(sender__in=friends))
        )
        .annotate(last_message_id=Max('id'))
        .values('last_message_id')
    )

    last_message_ids = [item['last_message_id'] for item in last_messages]
    last_messages = Message.objects.filter(id__in=last_message_ids)

    # Создать список друзей с последними сообщениями
    friends_with_last_messages = []
    for friend in friends:
        last_message = next((msg for msg in last_messages if msg.sender == friend or msg.recipient == friend), None)
        friends_with_last_messages.append({
            'friend': friend,
            'last_message': last_message
        })

    return render(request, 'chat/chat_list.html', {
        'friends_with_last_messages': friends_with_last_messages
    })


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    return redirect('chat:chat', username=other_user.username)
