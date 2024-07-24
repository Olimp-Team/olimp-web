from django import forms
from .models import Recommendation
from users.models import User
from main.models import Olympiad


class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['child', 'Olympiad']
        labels = {
            'child': 'Ученик',
            'Olympiad': 'Олимпиада',
        }
        widgets = {
            'child': forms.Select(attrs={'class': 'form-select block w-full mt-1', 'id': 'child-select'}),
            'Olympiad': forms.Select(attrs={'class': 'form-select block w-full mt-1', 'id': 'olympiad-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RecommendationForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['child'].queryset = User.objects.filter(is_child=True, school=user.school)
            self.fields['Olympiad'].queryset = Olympiad.objects.none()

        if 'child' in self.data:
            try:
                child_id = int(self.data.get('child'))
                child = User.objects.get(pk=child_id)
                self.fields['Olympiad'].queryset = Olympiad.objects.filter(
                    class_olympiad=child.classroom.number, stage__name='Школьный')
            except (ValueError, TypeError, User.DoesNotExist):
                pass  # оставляем поле Olympiad пустым
        elif self.instance.pk:
            self.fields['Olympiad'].queryset = self.instance.child.classroom.olympiad_set.all()
