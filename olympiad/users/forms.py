from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from django.forms import formset_factory
from users.models import User

from main.models import Classroom


class UserLoginForm(AuthenticationForm):
    # Форма для авторизации пользователя
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-control',
        'placeholder': 'Введите имя пользователя',
        'id': "login-input",
        'name': "login"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login',
        'placeholder': 'Введите пароль',
        'type': 'password',
        'id': 'password-input',
        'name': 'password'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    # Форма для смены имени пользователя, почты, аватарки на странице профиля
    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': "input",
        'id': "nameedit",
        'placeholder': "Введите имя пользователя",
        'name': "nameedit",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'type': "input",
        'id': "emailedit",
        'placeholder': "Введите свою почту",
        'name': "emailedit",
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': "newphoto",
        # 'type': "button",
        # 'value': "Загрузить новое фото",

    }), required=False)

    class Meta:
        model = User
        fields = ('image', 'username', 'email')


class NewChildForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'is_child', 'classroom', 'password',
            'gender')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин ученика"
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите отчество ученика"
    }))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите дату рождения ученика"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите пароль ученика"
    }))
    image = forms.ImageField(widget=forms.TextInput(attrs={
        'type': "submit",
        'value': "Загрузить новое фото",
        'class': "savenewphoto"
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите фамилию ученика",
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите имя ученика"
    }))
    at_obj = User()
    gender = forms.CharField(
        widget=forms.Select(
            choices=((at_obj, at_obj.name) for at_obj in at_obj.get_types())
        )
    )
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите пароль ученика"
    }))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите пароль ученика"
    }))


class NewTeacherForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'is_teacher', 'classroom_guide', 'subject',
            'post_job_teacher')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин ученика"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин ученика"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин ученика"
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин ученика"
    }))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин ученика"
    }))
    classroom_guide = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    subject = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    post_job_teacher = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))


class NewAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'is_admin')

    username = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    is_admin = forms.BooleanField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
