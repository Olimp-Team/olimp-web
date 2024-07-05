from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from main.models import *
from .forms import *
from django.contrib import messages


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


class ClassroomListView(View):
    def get(self, request):
        graduated = request.GET.get('graduated') == '1'
        if graduated:
            classrooms = Classroom.objects.filter(is_graduated=True).order_by('number', 'letter')
            context_title = "Выпустившиеся классы"
        else:
            classrooms = Classroom.objects.filter(is_graduated=False).order_by('number', 'letter')
            context_title = "Текущие классы"
        return render(request, 'list_classroom/list_classroom.html', {
            'classrooms': classrooms,
            'graduated': graduated,
            'context_title': context_title
        })


class PromoteAllClassroomsView(View):
    def get(self, request):
        return render(request, 'list_classroom/promote_all_classrooms_confirm.html')

    def post(self, request):
        classrooms = Classroom.objects.filter(is_graduated=False)
        for classroom in classrooms:
            classroom.promote()
        messages.success(request, 'Все классы успешно продвинуты.')
        return redirect('classroom:list_classroom')


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


class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classroom_add/classroom_form.html'
    success_url = reverse_lazy('classroom:list_classroom')


class ClassroomUpdateView(UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classroom_add/classroom_form.html'
    success_url = reverse_lazy('classroom:list_classroom')


class ClassroomDeleteView(DeleteView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'classroom_add/classroom_confirm_delete.html'
    success_url = reverse_lazy('classroom:list_classroom')
