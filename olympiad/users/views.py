from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.forms import UserLoginForm, UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def login(request):
    """Модель представления для входа"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile'))

    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, "auth/auth.html", context)


@login_required
def profile(request):
    """Модель представления для отображения профиля пользователя"""
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'profile/profile.html', context)


def redirect(request):
    """Модель представления для перенаправления с главной страницы на страницу авторизации"""
    return HttpResponseRedirect(reverse('users:login'))


@login_required
def logout(request):
    """Модель представления для выхода"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))


@login_required
def password_change(request):
    """Модель представления для смены пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль сменен успешно')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
        context = {'form': form}
        return render(request, 'password_change/password_change.html', context)
