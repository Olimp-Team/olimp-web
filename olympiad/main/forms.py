from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from olympiad.main.models import Classroom


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
