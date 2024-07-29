from django import forms
from .models import School
from users.models import User

class SchoolRegistrationForm(forms.ModelForm):
    """
    Форма регистрации школы, включающая создание администратора школы.
    """
    admin_username = forms.CharField(
        max_length=150,
        required=True,
        label='Имя пользователя администратора'
    )
    admin_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Пароль администратора'
    )
    admin_email = forms.EmailField(
        required=True,
        label='Email администратора'
    )
    admin_first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Имя администратора'
    )
    admin_last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Фамилия администратора'
    )

    class Meta:
        model = School
        fields = ['name', 'address', 'contact_email', 'contact_phone']
        labels = {
            'name': 'Название школы',
            'address': 'Адрес',
            'contact_email': 'Контактный email',
            'contact_phone': 'Контактный телефон',
        }

    def save(self, commit=True):
        """
        Сохраняет данные формы, создавая школу и администратора школы.
        """
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
