from django import forms
from .models import School
from users.models import *


class SchoolRegistrationForm(forms.ModelForm):
    admin_username = forms.CharField(max_length=150, required=True)
    admin_password = forms.CharField(widget=forms.PasswordInput, required=True)
    admin_email = forms.EmailField(required=True)
    admin_first_name = forms.CharField(max_length=150, required=True)
    admin_last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = School
        fields = ['name', 'address', 'contact_email', 'contact_phone']

    def save(self, commit=True):
        school = super().save(commit=commit)
        admin_user = User.objects.create(
            username=self.cleaned_data['admin_username'],
            email=self.cleaned_data['admin_email'],
            first_name=self.cleaned_data['admin_first_name'],
            last_name=self.cleaned_data['admin_last_name'],
            is_admin=True,
            school=school
        )
        admin_user.set_password(self.cleaned_data['admin_password'])
        if commit:
            admin_user.save()
        return school
