# users/views.py

from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewChildForm
from .mixins import AdminRequiredMixin
from main.models import *
from classroom.models import *

class AuthLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:home'))
        form = UserLoginForm()
        context = {'form': form}
        return render(request, "auth/auth 2.html", context)

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            school = form.cleaned_data['school']
            user = auth.authenticate(username=username, password=password)
            if user and user.school == school:
                auth.login(request, user)
                remember_me = request.POST.get('remember_me', None)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 недели
                else:
                    request.session.set_expiry(0)  # Закрыть сессию после закрытия браузера
                return HttpResponseRedirect(reverse('main:home'))
        context = {'form': form}
        return render(request, "auth/auth 2.html", context)


class start_page(View):
    def get(self, request):
        return render(request, 'start_page/start_page.html')


@login_required
def logout(request):
    """Модель представления для выхода"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class PasswordChange(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        context = {'form': form}
        return render(request, 'password_change/password_change.html', context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль сменен успешно')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)


class CreateAdmin(AdminRequiredMixin, View):
    def get(self, request):
        form = NewAdminForm()
        context = {'form': form}
        return render(request, 'add_admin/add_admin.html', context)

    def post(self, request):
        form = NewAdminForm(data=request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.is_admin = True
            admin.school = request.user.school
            admin.save()
            return HttpResponseRedirect(reverse('users:admin_list'))
        context = {'form': form}
        return render(request, 'add_admin/add_admin.html', context)


class CreateChild(AdminRequiredMixin, View):
    def get(self, request):
        form = NewChildForm()
        context = {'form': form}
        return render(request, 'add_students/add_students.html', context)

    def post(self, request):
        form = NewChildForm(data=request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.is_child = True
            child.school = request.user.school
            child.save()
            classroom = form.cleaned_data['classroom']
            Classroom.objects.get(id=classroom.id).child.add(child)
            return HttpResponseRedirect(reverse('classroom:list_classroom'))
        context = {'form': form}
        return render(request, 'add_students/add_students.html', context)


class CreateTeacher(AdminRequiredMixin, View):
    def get(self, request):
        form = NewTeacherForm()
        context = {'form': form}
        return render(request, 'add_teacher/add_teacher.html', context)

    def post(self, request):
        form = NewTeacherForm(data=request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.school = request.user.school
            teacher.save()
            form.save_m2m()  # Ensure M2M fields are saved
            return HttpResponseRedirect(reverse('users:teacher_list'))
        context = {'form': form}
        return render(request, 'add_teacher/add_teacher.html', context)


class TeacherListView(AdminRequiredMixin, View):
    def get(self, request):
        teachers = User.objects.filter(is_teacher=True, school=request.user.school)
        context = {'teachers': teachers}
        return render(request, 'teacher_list.html', context)


class AdminListView(AdminRequiredMixin, View):
    def get(self, request):
        admins = User.objects.filter(is_admin=True, school=request.user.school)
        context = {'admins': admins}
        return render(request, 'admin_list.html', context)


# @login_required
# def update_telegram_id(request):
#     if request.method == 'POST':
#         form = TelegramIDForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # Или куда хотите перенаправить после сохранения
#     else:
#         form = TelegramIDForm(instance=request.user)
#
#     return render(request, 'update_telegram_id.html', {'form': form})
