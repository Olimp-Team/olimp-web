from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponseNotFound
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import *
from users.forms import NewChildForm, NewTeacherForm, NewAdminForm
from .decorators import *
from .forms import ResultCreateFrom
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


def page_not_found(request, exception):
    return HttpResponseNotFound('Sorry, you are not allowed to see this page.')


class HomePage(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'homepage/homepage.html', )


########################################################################################################################
# Страницы учеников

########################################################################################################################
# Страницы учителей

class ChildrenListTeacher(View, LoginRequiredMixin):
    def get(self, request, Classroom_id):
        if request.user.teacher:
            classroom = Classroom.objects.get(id=Classroom_id)
            classroom_children = User.objects.filter(classroom_id=Classroom_id)
            context = {
                'classroom': classroom,
                'child': classroom_children
            }
            return render(request, 'children_list_teacher/children_list_teacher.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        pass


class TeacherClassroomGuide(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            classroom_teacher = Classroom.objects.filter(teacher__classroom_guide=request.user.classroom_guide)
            context = {
                'classroom_teacher': classroom_teacher
            }
            return render(request, 'list_classroom_teacher/list_classroom.html', context)


########################################################################################################################
# Страницы администратора

class ListOlympiad(TemplateView, AdminRequiredMixin):
    def get(self, request, *args, **kwargs):
        context = {
            'olympiad': Olympiad.objects.filter()
        }
        return render(request, 'list_olympiad/list_olympiad.html', context)


class OlympiadDelete(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request, Olympiad_id):
        olympiad = Olympiad.objects.get(id=Olympiad_id)
        olympiad.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def post(self, request):
        pass


class ChildRemoveAdmin(View, LoginRequiredMixin):
    def get(self, request, User_id):
        user_id = User.objects.get(id=User_id)
        user_id.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ListClassroom(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request):
        classroom = Classroom.objects.all()
        return render(request, 'list_classroom/list_classroom.html', context={'classroom': classroom})

    def post(self, request):
        pass


class ResultListOlympiad(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request):
        olymp = Register_admin.objects.all()
        child_admin_count = Register_admin.objects.all().count()
        context = {
            'olymp': olymp,
            'child_admin_count': child_admin_count
        }
        return render(request, 'result-list-olympiad/list-olympiad.html', context)


class Result(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request, olymp_id):
        register_olymp = Register_admin.objects.filter(Olympiad_admin_id=olymp_id)
        context = {
            'register_olymp': register_olymp,
            'register_olympiad': Register_admin.objects.filter(
                Olympiad_admin_id=olymp_id).first(),
        }
        return render(request, 'result-history/result-history.html', context)

    def post(self, request, olymp_id):
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


class ChildClassroomListAdmin(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request, Classroom_id):
        classroom = Classroom.objects.get(id=Classroom_id)
        classroom_children = User.objects.filter(classroom_id=Classroom_id)
        context = {
            'classroom': classroom,
            'child': classroom_children
        }
        return render(request, 'children_list_admin/children_list_admin.html', context)

    def post(self, request):
        pass
