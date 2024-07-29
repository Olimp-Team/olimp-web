from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import RegisterAdmin
from result.models import Result
from main.models import Olympiad

class ExcelUploadForm(forms.Form):
    """
    Форма для загрузки Excel файла.
    Используется для импорта данных из Excel в систему.
    """
    excel_file = forms.FileField(label='Загрузить Excel файл')

class OlympiadForm(forms.ModelForm):
    """
    Форма для создания и редактирования олимпиады.
    Использует модель Olympiad и включает все ее поля.
    """
    class Meta:
        model = Olympiad
        fields = '__all__'
        labels = {
            'name': 'Название олимпиады',
            'description': 'Описание олимпиады',
            'category': 'Категория олимпиады',
            'level': 'Уровень олимпиады',
            'stage': 'Этап олимпиады',
            'subject': 'Школьный предмет',
            'class_olympiad': 'Класс олимпиады',
            'date': 'Дата проведения',
            'time': 'Время проведения',
            'location': 'Место проведения',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
