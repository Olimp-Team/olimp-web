# chat/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    return render(request, 'chat/chat.html', {'other_user': other_user})