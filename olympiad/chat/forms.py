from django import forms
from users.models import *
from .models import *


class MessageForm(forms.ModelForm):
    class Meta:
        # model = Message
        fields = ['recipient', 'content']

    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label="Recipient")


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }
