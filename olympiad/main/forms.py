from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from main.models import *


class ExcelUploadForm(forms.Form):
    """Форма для импорта excel файла"""
    excel_file = forms.FileField()


class NewClassroomForm(UserCreationForm):
    class Meta:
        model = Classroom
        fields = ('number', 'letter', 'teacher', 'child')

    number = forms.IntegerField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    letter = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    teacher = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    child = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))


PARTICIPANT = 'У'
PRIZE = 'ПР'
WINNER = 'ПОБД'
STATUSRES = [
    (PARTICIPANT, 'Участник'),
    (PRIZE, 'Призер'),
    (WINNER, 'Победитель')

]


class ChoiceForm(forms.Form):
    class Meta:
        model = Result
        fields = 'status_result', 'points'

    status_result = forms.ChoiceField(choices=STATUSRES, widget=forms.Select(attrs={
        'id': 'select',
    }))
    points = forms.IntegerField(widget=forms.NumberInput(attrs={
        'type': 'number',
    }))


class NewOlympiadForm(UserCreationForm):
    class Meta:
        model = Classroom
        fields = ('name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad')

    name = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    category = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    level = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    stage = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    subject = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    class_olympiad = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
