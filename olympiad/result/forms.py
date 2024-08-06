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


### TEST


class ResultForm(forms.ModelForm):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all(), required=False,
                                       widget=forms.Select(attrs={'class': 'select2'}))

    class Meta:
        model = Result
        fields = ['classroom', 'info_children', 'info_olympiad', 'points', 'status_result', 'advanced', 'school']
        widgets = {
            'info_children': forms.Select(attrs={'class': 'select2'}),
            'info_olympiad': forms.Select(attrs={'class': 'select2'}),
            'points': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Количество очков'}),
            'status_result': forms.Select(attrs={'class': 'input'}),
            'advanced': forms.CheckboxInput(attrs={'class': 'input'}),
            'school': forms.Select(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['info_children'].queryset = User.objects.none()
        self.fields['info_olympiad'].queryset = Olympiad.objects.none()

        if 'classroom' in self.data:
            try:
                classroom_id = int(self.data.get('classroom'))
                self.fields['info_children'].queryset = User.objects.filter(classroom_id=classroom_id,
                                                                            is_child=True).order_by('last_name')
            except (ValueError, TypeError):
                pass

        if 'info_children' in self.data:
            try:
                user_id = int(self.data.get('info_children'))
                self.fields['info_olympiad'].queryset = Olympiad.objects.filter(
                    class_olympiad__exact=self.fields['classroom'].queryset.first().number).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['info_olympiad'].queryset = self.instance.info_children.olympiad_set.order_by('name')
