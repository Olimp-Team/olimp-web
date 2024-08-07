from django import forms
from classroom.models import *
from users.models import User


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClassroomForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.get_teachers()
        self.fields['child'].queryset = User.get_children()
