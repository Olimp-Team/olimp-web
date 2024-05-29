from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import *
from users.forms import NewChildForm
from .decorators import *
from .models import Register, Register_admin
from .forms import ResultCreateFrom
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


# Страницы учителей
class StudentApp(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            reg = Register_send.objects.filter(teacher_send__classroom_guide=request.user.classroom_guide,
                                               status_teacher=False)
            context = {
                'register': reg
            }
            return render(request, 'student-applications/student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class TeacherClassroomGuide(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            classroom_teacher = Classroom.objects.filter(teacher__classroom_guide=request.user.classroom_guide)
            context = {
                'classroom_teacher': classroom_teacher
            }
            return render(request, 'list_classroom_teacher/list_classroom.html', context)


class ChildrenListTeacher(View, LoginRequiredMixin):
    def get(self, request, Classroom_id):
        if request.user.teacher:
            classroom = Classroom.objects.get(id=Classroom_id)
            classroom_children = User.objects.filter(classroom_id=Classroom_id)
            context = {
                'classroom': classroom,
                'child': classroom_children
            }
            return render(request, 'children_list_teacher/student_applications_admin.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        pass


class RegisterRemoveTeacher(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_teacher:
            reg = Register_send.objects.filter(teacher_send__classroom_guide=request.user.classroom_guide,
                                               status_teacher=False)
            context = {
                'register': reg
            }
            return render(request, 'student-applications/student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class RegisterSendTeacher(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            RST = [
                Register_admin(
                    teacher_admin=i.teacher_send,
                    child_admin=i.child_send,
                    Olympiad_admin=i.Olympiad_send,

                )
                for i in
                Register_send.objects.filter(child_send__classroom__exact=request.user.classroom_guide,
                                             status_teacher=False)
            ]
            Register_admin.objects.bulk_create(RST)
            Register_send.objects.filter(child_send__classroom__teacher=request.user).update(status_teacher=True)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()
