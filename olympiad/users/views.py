from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash, views as auth_views
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    UserLoginForm,
    NewAdminForm,
    NewChildForm,
    NewTeacherForm,
    UserForm, CustomPasswordResetForm,

)
from .mixins import AdminRequiredMixin
from classroom.models import Classroom
from users.models import User


class AuthLogin(View):
    """Представление для входа пользователей."""

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:home'))
        form = UserLoginForm()
        return render(request, "auth/auth 2.html", {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            school = form.cleaned_data['school']
            user = auth.authenticate(username=username, password=password)
            if user and user.school == school:
                auth.login(request, user)
                request.session.set_expiry(1209600 if request.POST.get('remember_me') else 0)
                return HttpResponseRedirect(reverse('main:home'))
        return render(request, "auth/auth 2.html", {'form': form})


class StartPage(View):
    """Представление для главной страницы сайта."""

    def get(self, request):
        return render(request, 'start_page/start_page.html')


@login_required
def logout(request):
    """Выход из системы."""
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class PasswordChange(View):
    """Представление для изменения пароля."""

    def get(self, request):
        form = CustomPasswordResetForm(request.user)
        return render(request, 'password_change/password_change.html', {'form': form})

    def post(self, request):
        form = CustomPasswordResetForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен.')
            return HttpResponseRedirect(reverse('users:login'))
        messages.error(request, 'Ошибка изменения пароля.')
        return render(request, 'password_change/password_change.html', {'form': form})


class CreateAdmin(AdminRequiredMixin, View):
    """Представление для создания администратора."""

    def get(self, request):
        form = NewAdminForm()
        return render(request, 'add_admin/add_admin.html', {'form': form})

    def post(self, request):
        form = NewAdminForm(data=request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.is_admin = True
            admin.school = request.user.school
            admin.save()
            return HttpResponseRedirect(reverse('users:admin_list'))
        return render(request, 'add_admin/add_admin.html', {'form': form})


class CreateChild(AdminRequiredMixin, View):
    """Представление для создания ученика."""

    def get(self, request):
        form = NewChildForm()
        return render(request, 'add_students/add_students.html', {'form': form})

    def post(self, request):
        form = NewChildForm(data=request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.is_child = True
            child.school = request.user.school
            child.save()
            classroom = form.cleaned_data['classroom']
            classroom.child.add(child)
            return HttpResponseRedirect(reverse('classroom:list_classroom'))
        return render(request, 'add_students/add_students.html', {'form': form})


class CreateTeacher(AdminRequiredMixin, View):
    """Представление для создания учителя."""

    def get(self, request):
        form = NewTeacherForm()
        return render(request, 'add_teacher/add_teacher.html', {'form': form})

    def post(self, request):
        form = NewTeacherForm(data=request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.school = request.user.school
            teacher.save()
            form.save_m2m()  # Сохраняем связи M2M
            return HttpResponseRedirect(reverse('users:teacher_list'))
        return render(request, 'add_teacher/add_teacher.html', {'form': form})


class TeacherListView(AdminRequiredMixin, View):
    """Представление для списка учителей."""

    def get(self, request):
        teachers = User.objects.filter(is_teacher=True, school=request.user.school)
        return render(request, 'teacher_list.html', {'teachers': teachers})


class AdminListView(AdminRequiredMixin, View):
    """Представление для списка администраторов."""

    def get(self, request):
        admins = User.objects.filter(is_admin=True, school=request.user.school)
        return render(request, 'admin_list.html', {'admins': admins})


class EditTeacherView(AdminRequiredMixin, View):
    """Представление для редактирования учителя."""

    def get(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, is_teacher=True, school=request.user.school)
        form = UserForm(instance=teacher)
        return render(request, 'edit_teacher.html', {'form': form, 'teacher': teacher})

    def post(self, request, pk):
        teacher = get_object_or_404(User, pk=pk, is_teacher=True, school=request.user.school)
        form = UserForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('users:teacher_list')
        return render(request, 'edit_teacher.html', {'form': form, 'teacher': teacher})


class EditAdminView(AdminRequiredMixin, View):
    """Представление для редактирования администратора."""

    def get(self, request, pk):
        admin = get_object_or_404(User, pk=pk, is_admin=True, school=request.user.school)
        form = UserForm(instance=admin)
        return render(request, 'edit_admin.html', {'form': form, 'admin': admin})

    def post(self, request, pk):
        admin = get_object_or_404(User, pk=pk, is_admin=True, school=request.user.school)
        form = UserForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('users:admin_list')
        return render(request, 'edit_admin.html', {'form': form, 'admin': admin})


class DeleteUserView(AdminRequiredMixin, View):
    """Представление для удаления пользователя."""

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk, school=request.user.school)
        user.delete()
        if user.is_teacher:
            return redirect('users:teacher_list')
        elif user.is_admin:
            return redirect('users:admin_list')
        return HttpResponseForbidden()
