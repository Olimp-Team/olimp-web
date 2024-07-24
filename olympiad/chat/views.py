from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Q, Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from friendship.models import Friend
from .forms import *

User = get_user_model()


@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
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
    friends = Friend.objects.friends(current_user)

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

    friends_with_last_messages = [
        {'friend': friend,
         'last_message': next((msg for msg in last_messages if msg.sender == friend or msg.recipient == friend), None)}
        for friend in friends
    ]

    return render(request, 'chat/chat_list.html', {
        'friends_with_last_messages': friends_with_last_messages
    })


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    return redirect('chat:chat', username=other_user.username)


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('chat:group_detail', group_id=group.id)
    else:
        form = GroupForm()
    return render(request, 'chat/create_group.html', {'form': form})


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')
    return render(request, 'chat/group_detail.html', {'group': group, 'messages': messages})
