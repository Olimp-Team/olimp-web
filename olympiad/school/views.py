from django.shortcuts import render, redirect
from .forms import SchoolRegistrationForm
from django.contrib.auth import login, authenticate

def register_school(request):
    """
    Представление для регистрации новой школы и создания администратора.
    """
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            school = form.save()  # Сохранение формы и создание записи школы
            admin_user = authenticate(
                username=form.cleaned_data['admin_username'],
                password=form.cleaned_data['admin_password']
            )  # Аутентификация нового администратора
            if admin_user:
                login(request, admin_user)  # Вход нового администратора
                return redirect('users:login')  # Перенаправление на страницу входа пользователя
    else:
        form = SchoolRegistrationForm()  # Создание новой пустой формы
    return render(request, 'register_school.html', {'form': form})  # Отображение страницы регистрации
