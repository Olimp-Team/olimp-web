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


class NewChild(UserCreationForm):
    class Meta:
        model = User
        fields = ('image', 'last_name', 'first_name', 'surname', 'birth_date', 'gender', 'classroom',)

    image = forms.ImageField(widget=forms.TextInput(attrs={
        'type': "submit",
        'value': "Загрузить новое фото",
        'class': "savenewphoto"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите фамилию ученика",
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите имя ученика"
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
