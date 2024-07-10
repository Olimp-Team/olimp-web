from django import forms
from .models import Result
from users.models import *
from main.models import *
from register.models import *


class OlympiadResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['info_children', 'info_olympiad', 'points', 'status_result']

    def __init__(self, *args, **kwargs):
        super(OlympiadResultForm, self).__init__(*args, **kwargs)
        # Фильтр для поля info_children
        registered_children_ids = Register_admin.objects.values_list('child_admin_id', flat=True)
        self.fields['info_children'].queryset = User.objects.filter(is_child=True, id__in=registered_children_ids)
        self.fields['info_olympiad'].queryset = Olympiad.objects.none()  # Пустой список изначально

        # Добавляем стилизацию к полям формы
        self.fields['info_children'].widget.attrs.update({'class': 'block w-full mt-1 p-2 border rounded student-select'})
        self.fields['info_olympiad'].widget.attrs.update({'class': 'block w-full mt-1 p-2 border rounded olympiad-select'})
        self.fields['points'].widget.attrs.update({'class': 'block w-full mt-1 p-2 border rounded'})
        self.fields['status_result'].widget.attrs.update({'class': 'block w-full mt-1 p-2 border rounded'})

    info_children = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Начальное пустое значение
        widget=forms.Select()
    )
    info_olympiad = forms.ModelChoiceField(
        queryset=Olympiad.objects.none(),
        widget=forms.Select()
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
