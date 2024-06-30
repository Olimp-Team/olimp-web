from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import MessageForm


class InboxView(LoginRequiredMixin, View):
    def get(self, request):
        messages = Message.objects.filter(recipient=request.user)
        return render(request, 'chat/inbox.html', {'messages': messages})


class SendMessageView(LoginRequiredMixin, View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'chat/send_message.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
        return render(request, 'chat/send_message.html', {'form': form})
