from django.shortcuts import render, HttpResponseRedirect
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
from main.models import Classroom


class AuthLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:home'))
        form = UserLoginForm()
        context = {'form': form}
        return render(request, "auth/auth.html", context)

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            remember_me = request.POST.get('remember_me', None)
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 недели
                else:
                    request.session.set_expiry(0)  # Закрыть сессию после закрытия браузера
                return HttpResponseRedirect(reverse('main:home'))
        context = {'form': form}
        return render(request, "auth/auth.html", context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profile/profile.html', context)

    def post(self, request):
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
        context = {'form': form}
        return render(request, 'profile/profile.html', context)


# def redirect(request):
#     """Модель представления для перенаправления с главной страницы на страницу авторизации"""
#     return HttpResponseRedirect(reverse('users:login'))

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
            teacher.save()
            form.save_m2m()  # Ensure M2M fields are saved
            return HttpResponseRedirect(reverse('users:teacher_list'))
        context = {'form': form}
        return render(request, 'add_teacher/add_teacher.html', context)


class TeacherListView(AdminRequiredMixin, View):
    def get(self, request):
        teachers = User.objects.filter(is_teacher=True)
        context = {'teachers': teachers}
        return render(request, 'teacher_list.html', context)


class AdminListView(AdminRequiredMixin, View):
    def get(self, request):
        admins = User.objects.filter(is_admin=True)
        context = {'admins': admins}
        return render(request, 'admin_list.html', context)
