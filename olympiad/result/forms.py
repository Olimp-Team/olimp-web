from django import forms
from .models import Result
from users.models import *
from main.models import *
from register.models import *


class OlympiadResultForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_child=True,
            id__in=Register_admin.objects.values_list('child_admin_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'student-select'}),
        label='Ученик'
    )
    olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.filter(
            id__in=Register_admin.objects.values_list('Olympiad_admin_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'olympiad-select'}),
        label='Олимпиада'
    )
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'score-input'}), label='Результат')
    status = forms.ChoiceField(
        choices=Result.STATUSRES,
        widget=forms.Select(attrs={'class': 'status-select'}),
        label='Статус'
    )

from .widgets import CustomModelChoiceField


class OlympiadResultClassForm(forms.Form):
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.filter(
            id__in=Register_admin.objects.values_list('child_admin__classroom_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'classroom-select'}),
        label='Класс'
    )
    olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.filter(
            id__in=Register_admin.objects.values_list('Olympiad_admin_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'olympiad-select'}),
        label='Олимпиада'
    )
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'score-input'}), label='Результат')
    status = forms.ChoiceField(
        choices=Result.STATUSRES,
        widget=forms.Select(attrs={'class': 'status-select'}),
        label='Статус'
    )
