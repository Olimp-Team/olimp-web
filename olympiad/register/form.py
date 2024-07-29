from django import forms
from .models import Recommendation
from users.models import User
from main.models import Olympiad


class RecommendationForm(forms.ModelForm):
    """Форма для создания рекомендаций на олимпиады для учеников"""

    class Meta:
        model = Recommendation
        fields = ['child', 'olympiad']
        labels = {
            'child': 'Ученик',
            'Olympiad': 'Олимпиада',
        }
        widgets = {
            'child': forms.Select(attrs={'class': 'form-select block w-full mt-1', 'id': 'child-select'}),
            'Olympiad': forms.Select(attrs={'class': 'form-select block w-full mt-1', 'id': 'olympiad-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получение текущего пользователя
        super(RecommendationForm, self).__init__(*args, **kwargs)

        if user:
            # Фильтрация учеников по школе текущего пользователя
            self.fields['child'].queryset = User.objects.filter(is_child=True, school=user.school)
            self.fields['Olympiad'].queryset = Olympiad.objects.none()

        if 'child' in self.data:
            try:
                child_id = int(self.data.get('child'))
                child = User.objects.get(pk=child_id)
                # Фильтрация олимпиад по классу ученика и этапу "Школьный"
                self.fields['Olympiad'].queryset = Olympiad.objects.filter(
                    class_olympiad=child.classroom.number, stage__name='Школьный')
            except (ValueError, TypeError, User.DoesNotExist):
                pass  # оставляем поле Olympiad пустым, если ошибка

        elif self.instance.pk:
            # Заполнение поля Olympiad для существующей рекомендации
            self.fields['Olympiad'].queryset = self.instance.child.classroom.olympiad_set.all()
