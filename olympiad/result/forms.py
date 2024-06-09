from django import forms
from .models import Result
from users.models import *
from main.models import *


class OlympiadResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['info_children', 'info_olympiad', 'points', 'status_result']

    info_children = forms.ModelChoiceField(
        queryset=User.objects.filter(is_child=True),
        widget=forms.Select(attrs={'class': 'student-select'})
    )
    info_olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.all(),
        widget=forms.Select(attrs={'class': 'olympiad-select'})
    )


class OlympiadResultClassForm(forms.Form):
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        widget=forms.Select(attrs={'class': 'classroom-select'})
    )
    olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.all(),
        widget=forms.Select(attrs={'class': 'olympiad-select'})
    )
    score = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'score-input'}))
    status = forms.ChoiceField(
        choices=Result.STATUSRES,
        widget=forms.Select(attrs={'class': 'status-select'})
    )



