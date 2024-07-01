from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import *
from result.models import *
from main.models import *




class ExcelUploadForm(forms.Form):
    """Форма для импорта excel файла"""
    excel_file = forms.FileField()


class OlympiadForm(forms.ModelForm):
    class Meta:
        model = Olympiad
        fields = '__all__'


