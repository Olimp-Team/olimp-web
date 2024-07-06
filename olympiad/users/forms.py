from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django import forms
from users.models import User
from main.models import *


class UserLoginForm(AuthenticationForm):
    # Форма для авторизации пользователя
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': "login",
        'name': "login",
        'type': "login",
        'autocomplete': "login",
        'required': True,
        'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "password",
        'name': "password",
        'type': "password",
        'autocomplete': "current-password",
        'required': True,
        'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
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


class NewChildForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'is_child', 'classroom', 'password',
            'gender'
        )

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
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'type': "submit",
        'value': "Загрузить новое фото",
        'class': "savenewphoto"
    }), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите фамилию ученика"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': "search",
        'class': "vvodinfo",
        'placeholder': "Введите имя ученика"
    }))
    gender = forms.ChoiceField(choices=[(gender, gender) for gender in User().get_types()])

    def save(self, commit=True):
        user = super(NewChildForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class NewTeacherForm(forms.ModelForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    classroom_guide = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        widget=forms.RadioSelect,  # Или другой подходящий виджет
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'classroom_guide', 'subject',
            'post_job_teacher', 'password', 'gender'
        )

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин учителя"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите имя учителя"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите фамилию учителя"
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите отчество учителя"
    }))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите дату рождения учителя"
    }))
    post_job_teacher = forms.ModelMultipleChoiceField(
        queryset=Post.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': "vvodinfo"
        }),
        required=True
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите пароль учителя"
    }))

    def save(self, commit=True):
        user = super(NewTeacherForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class NewAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'password', 'gender'
        )

    username = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите логин администратора"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите имя администратора"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите фамилию администратора"
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите отчество администратора"
    }))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите дату рождения администратора"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'search',
        'class': "vvodinfo",
        'placeholder': "Введите пароль администратора"
    }))

    def save(self, commit=True):
        user = super(NewAdminForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class NewOlympiadForm(UserCreationForm):
    class Meta:
        model = Classroom
        fields = ('name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad')

    name = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "input" пример
    }))
    category = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    level = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    stage = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    subject = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))
    class_olympiad = forms.MultipleChoiceField(widget=forms.TextInput(attrs={  # УЗНАТЬ МЕТОД ФОРМЫ
        # 'type': "input" пример
    }))


from django.contrib.auth.forms import PasswordResetForm


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
