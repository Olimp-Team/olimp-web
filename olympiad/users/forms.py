from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordResetForm
from users.models import User
from main.models import Subject, Post, Category, LevelOlympiad, Stage
from school.models import School
from classroom.models import Classroom
import base64
from django.core.files.base import ContentFile


class UserLoginForm(AuthenticationForm):
    """Форма для входа пользователя"""
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
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=forms.Select(attrs={
        'id': "school",
        'name': "school",
        'required': True,
        'class': "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 select2",
    }), label='Школа')

    class Meta:
        model = User
        fields = ('username', 'password', 'school')


class UserProfileForm(UserChangeForm):
    """Форма профиля пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Введите имя пользователя"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "Введите свою почту"}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'id': "file-input"}), required=False)

    class Meta:
        model = User
        fields = ('image', 'username', 'email', 'birth_date', 'gender')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.birth_date:
            self.fields.pop('birth_date')


class NewChildForm(forms.ModelForm):
    """Форма для создания нового ученика"""
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'surname', 'birth_date', 'is_child', 'classroom', 'password', 'gender'
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
    gender = forms.ChoiceField(choices=User.GENDER_CHOICES)

    def save(self, commit=True):
        user = super(NewChildForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class NewTeacherForm(forms.ModelForm):
    """Форма для создания нового учителя"""
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
    """Форма для создания нового администратора"""
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
    """Форма для создания новой олимпиады"""
    class Meta:
        model = Classroom
        fields = ('name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad')

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Введите название олимпиады"
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Введите описание олимпиады"
    }))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'placeholder': "Выберите категорию олимпиады"
    }))
    level = forms.ModelChoiceField(queryset=LevelOlympiad.objects.all(), widget=forms.Select(attrs={
        'placeholder': "Выберите уровень олимпиады"
    }))
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), widget=forms.Select(attrs={
        'placeholder': "Выберите этап олимпиады"
    }))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={
        'placeholder': "Выберите предмет олимпиады"
    }))
    class_olympiad = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': "Введите класс олимпиады"
    }))


class CustomPasswordResetForm(PasswordResetForm):
    """Форма для сброса пароля"""
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))


class TelegramIDForm(forms.ModelForm):
    """Форма для ввода Telegram ID"""
    class Meta:
        model = User
        fields = ['telegram_id']
        widgets = {
            'telegram_id': forms.TextInput(attrs={'placeholder': 'Введите ваш Telegram ID'}),
        }


class UserForm(forms.ModelForm):
    """Форма для пользователя"""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input mt-1 block w-full'}))

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'surname', 'username', 'password', 'email', 'school', 'birth_date', 'gender']
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'surname': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'username': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input mt-1 block w-full'}),
            'school': forms.Select(attrs={'class': 'form-input mt-1 block w-full'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-input mt-1 block w-full', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select mt-1 block w-full'}),
        }
