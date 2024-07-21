from django.shortcuts import render, redirect
from .forms import SchoolRegistrationForm
from django.contrib.auth import login, authenticate


def register_school(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            school = form.save()
            admin_user = authenticate(
                username=form.cleaned_data['admin_username'],
                password=form.cleaned_data['admin_password']
            )
            if admin_user:
                login(request, admin_user)
                return redirect('dashboard')  # Замените 'dashboard' на ваш URL для панели администратора
    else:
        form = SchoolRegistrationForm()
    return render(request, 'register_school.html', {'form': form})