from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from users.models import Users


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
        model = Users
        fields = ('username', 'password')


# РЕГИСТРАЦИЮ СДЕАТЬ ЧУТЬ ПОЗЖЕ
# class UserRegisterForm(UserCreationForm):
#     class Meta:
#         model = Users
#         fields = (
#             'username', 'email', 'password1', 'password2', 'image', 'status_user', 'is_active', 'is_staff',
#             'is_superuser', 'first_name', 'last_name', 'surname', 'gender', 'birth_date', 'date_joined')


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
        model = Users
        fields = ('image', 'username', 'email')
