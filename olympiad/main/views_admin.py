from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import *
from users.forms import NewChildForm
from .decorators import *
from .models import Register_admin
from .forms import ResultCreateFrom
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


# Страницы администратора

class ListOlympiad(TemplateView, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request, *args, **kwargs):
        context = {
            'olympiad': Olympiad.objects.filter()
        }
        return render(request, 'list_olympiad/list_olympiad.html', context)


class OlympiadDelete(View, LoginRequiredMixin):
    def get(self, request, Olympiad_id):
        if request.user.is_admin:
            olympiad = Olympiad.objects.get(id=Olympiad_id)
            olympiad.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request):
        pass


class RegisterListClassroom(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            context = {
                'register': Register_admin.objects.all()
            }
            return render(request, 'applications-from-classroom-teachers/applications-from-classroom-teachers.html',
                          context)
        else:
            return HttpResponseForbidden()


class ChildRemoveAdmin(View, LoginRequiredMixin):
    def get(self, request, User_id):
        if request.user.is_admin:
            user_id = User.objects.get(id=User_id)
            user_id.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class StudentAdminApp(View, LoginRequiredMixin):
    def get(self, request, Classroom_id):
        if request.user.is_admin:
            classroom = Classroom.objects.get(id=Classroom_id)
            classroom_children = User.objects.filter(classroom_id=Classroom_id)
            context = {
                'classroom': classroom,
                'child': classroom_children
            }
            return render(request, 'student_applications_admin/student_applications_admin.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        pass


class ListClassroom(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            classroom = Classroom.objects.all()
            return render(request, 'list_classroom/list_classroom.html', context={'classroom': classroom})
        else:
            return HttpResponseForbidden()

    def post(self, request):
        pass


class ResultListOlympiad(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            olymp = Register_admin.objects.all()
            child_admin_count = Register_admin.objects.all().count()
            context = {
                'olymp': olymp,
                'child_admin_count': child_admin_count
            }
            return render(request, 'result-list-olympiad/list-olympiad.html', context)
        else:
            return HttpResponseForbidden()


class CreateAdmin(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            return render(request, 'add_admin/add_admin.html')
        else:
            return HttpResponseForbidden()


class CreateChildView(CreateView, LoginRequiredMixin):
    form_class = NewChildForm
    template_name = 'add_students/add_students.html'
    success_url = reverse_lazy('main:list_classroom')

    def form_valid(self, form):
        classroom = form.cleaned_data['classroom']
        form.save()
        return super().form_valid(form)


class CreateChild(View, LoginRequiredMixin):
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
            return HttpResponseRedirect(reverse('main:list_classroom'))
        context = {'form': form}
        return render(request, 'add_students/add_students.html', context)


class CreateTeacher(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            return render(request, 'add_teacher/add_teacher.html')
        else:
            return HttpResponseForbidden()


class Result(View, LoginRequiredMixin):
    def get(self, request, olymp_id):
        register_olymp = Register_admin.objects.filter(Olympiad_admin_id=olymp_id)
        context = {
            'register_olymp': register_olymp,
            'register_olympiad': Register_admin.objects.filter(
                Olympiad_admin_id=olymp_id).first(),
        }
        return render(request, 'result-history/result-history.html', context)

    def post(self, request, olymp_id):
        if request.user.is_admin:
            register_olymp = Register_admin.objects.filter(Olympiad_admin_id=olymp_id)
            form = ResultCreateFrom(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            form = ResultCreateFrom()
            context = {
                'form': form,
                'register_olymp': register_olymp,
                'register_olympiad': Register_admin.objects.filter(
                    Olympiad_admin_id=olymp_id).first(),
            }
            return render(request, 'result-history/result-history.html', context)
        else:
            return HttpResponseForbidden()
