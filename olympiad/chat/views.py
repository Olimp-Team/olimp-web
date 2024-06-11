from django.shortcuts import render
from .models import Group, Message
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, room_name):
    group, _ = Group.objects.get_or_create(name=room_name)
    messages = Message.objects.filter(group=group).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })
