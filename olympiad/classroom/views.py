from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from main.models import *


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


class ListClassroom(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request):
        classroom = Classroom.objects.all()
        return render(request, 'list_classroom/list_classroom.html', context={'classroom': classroom})

    def post(self, request):
        pass


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


class ChildRemoveAdmin(View, LoginRequiredMixin):
    def get(self, request, User_id):
        user_id = User.objects.get(id=User_id)
        user_id.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
