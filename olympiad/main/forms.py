from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from register.models import *
from result.models import *
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


class ResultCreateFrom(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status_result'].empty_label = 'Статус не выбран'

    class Meta:
        model = Result
        fields = 'status_result', 'points'

    status_result = forms.ChoiceField(choices=STATUSRES, widget=forms.Select(attrs={
        'id': 'select',
    }))
    points = forms.IntegerField(widget=forms.NumberInput(attrs={
        'type': 'number',
    }))



