from django import forms
from .models import Result
from users.models import User
from main.models import Olympiad
from register.models import RegisterAdmin
from classroom.models import Classroom


class OlympiadResultForm(forms.Form):
    """
    Форма для ввода результатов олимпиад для отдельного ученика.
    """
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_child=True,
            id__in=RegisterAdmin.objects.values_list('child_admin_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'student-select'}),
        label='Ученик'
    )
    olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.filter(
            id__in=RegisterAdmin.objects.values_list('olympiad_admin_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'olympiad-select'}),
        label='Олимпиада'
    )
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'score-input'}),
        label='Результат'
    )
    status = forms.ChoiceField(
        choices=Result.STATUSRES,
        widget=forms.Select(attrs={'class': 'status-select'}),
        label='Статус'
    )


class OlympiadResultClassForm(forms.Form):
    """
    Форма для ввода результатов олимпиад для класса.
    """
    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.filter(
            id__in=RegisterAdmin.objects.values_list('child_admin__classroom_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'classroom-select'}),
        label='Класс'
    )
    olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.filter(
            id__in=RegisterAdmin.objects.values_list('olympiad_admin_id', flat=True).distinct()
        ),
        widget=forms.Select(attrs={'class': 'olympiad-select'}),
        label='Олимпиада'
    )
    score = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'score-input'}),
        label='Результат'
    )
    status = forms.ChoiceField(
        choices=Result.STATUSRES,
        widget=forms.Select(attrs={'class': 'status-select'}),
        label='Статус'
    )
