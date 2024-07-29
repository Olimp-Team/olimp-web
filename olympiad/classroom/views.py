from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView, CreateView

from users.models import User
from users.mixins import AdminRequiredMixin
from classroom.models import Classroom
from .forms import ClassroomForm
from django.contrib import messages


class ChildrenListTeacher(LoginRequiredMixin, View):
    """Отображение списка детей для учителя в конкретном классе"""

    def get(self, request, Classroom_id):
        if request.user.is_teacher:
            classroom = get_object_or_404(Classroom, id=Classroom_id, school=request.user.school)
            classroom_children = User.objects.filter(classroom_id=Classroom_id, school=request.user.school)
            context = {
                'classroom': classroom,
                'children': classroom_children
            }
            return render(request, 'children_list_teacher/children_list_teacher.html', context)
        return HttpResponseForbidden()


class TeacherClassroomGuide(LoginRequiredMixin, View):
    """Отображение классов, закрепленных за учителем"""

    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            classrooms = Classroom.objects.filter(teacher=request.user, school=request.user.school)
            context = {
                'classrooms': classrooms
            }
            return render(request, 'list_classroom_teacher/list_classroom.html', context)
        return HttpResponseForbidden()


class ClassroomListView(LoginRequiredMixin, View):
    """Отображение списка классов с возможностью фильтрации по выпуску"""

    def get(self, request):
        graduated = request.GET.get('graduated') == '1'
        classrooms = Classroom.objects.filter(is_graduated=graduated, school=request.user.school).order_by('number', 'letter')
        context_title = "Выпустившиеся классы" if graduated else "Текущие классы"
        return render(request, 'list_classroom/list_classroom.html', {
            'classrooms': classrooms,
            'graduated': graduated,
            'context_title': context_title
        })


class PromoteAllClassroomsView(LoginRequiredMixin, View):
    """Продвижение всех классов на следующий уровень"""

    def get(self, request):
        return render(request, 'list_classroom/promote_all_classrooms_confirm.html')

    def post(self, request):
        classrooms = Classroom.objects.filter(is_graduated=False, school=request.user.school)
        for classroom in classrooms:
            classroom.promote()
        messages.success(request, 'Все классы успешно продвинуты.')
        return redirect('classroom:list_classroom')


class ChildClassroomListAdmin(LoginRequiredMixin, AdminRequiredMixin, View):
    """Отображение списка детей для администратора в конкретном классе"""

    def get(self, request, Classroom_id):
        classroom = get_object_or_404(Classroom, id=Classroom_id, school=request.user.school)
        classroom_children = User.objects.filter(classroom_id=Classroom_id, school=request.user.school)
        context = {
            'classroom': classroom,
            'children': classroom_children
        }
        return render(request, 'children_list_admin/children_list_admin.html', context)


class ChildExpelAdmin(LoginRequiredMixin, View):
    """Исключение ученика администратором"""

    def post(self, request, User_id):
        user = get_object_or_404(User, id=User_id, school=request.user.school)
        user.is_expelled = True
        user.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ChildReinstateAdmin(LoginRequiredMixin, View):
    """Восстановление ученика администратором"""

    def post(self, request, User_id):
        user = get_object_or_404(User, id=User_id, school=request.user.school)
        user.is_expelled = False
        user.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ChildRemoveAdmin(LoginRequiredMixin, View):
    """Удаление ученика администратором"""

    def get(self, request, User_id):
        user = get_object_or_404(User, id=User_id, school=request.user.school)
        user.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ClassroomCreateView(LoginRequiredMixin, CreateView):
    """Создание нового класса"""

    model = Classroom
    form_class = ClassroomForm
    template_name = 'classroom_add/classroom_form.html'
    success_url = reverse_lazy('classroom:list_classroom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_students'] = User.objects.filter(is_child=True, school=self.request.user.school)
        return context

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        response = super().form_valid(form)
        students_ids = self.request.POST.getlist('students')
        students = User.objects.filter(id__in=students_ids, is_child=True, school=self.request.user.school)
        self.object.child.set(students)
        return response


class ClassroomUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление информации о классе"""

    model = Classroom
    form_class = ClassroomForm
    template_name = 'classroom_add/classroom_form.html'
    success_url = reverse_lazy('classroom:list_classroom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_students'] = User.objects.filter(is_child=True, school=self.request.user.school)
        context['class_students'] = self.get_class_students()
        return context

    def get_class_students(self):
        classroom_id = self.kwargs.get('pk')
        if classroom_id:
            classroom = get_object_or_404(Classroom, pk=classroom_id, school=self.request.user.school)
            return classroom.child.all()
        return User.objects.none()

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        response = super().form_valid(form)
        students_ids = self.request.POST.getlist('students')
        students = User.objects.filter(id__in=students_ids, is_child=True, school=self.request.user.school)
        self.object.child.set(students)
        return response


class ClassroomDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление класса"""

    model = Classroom
    template_name = 'classroom_add/classroom_confirm_delete.html'
    success_url = reverse_lazy('classroom:list_classroom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_students'] = User.objects.filter(is_child=True, school=self.request.user.school)
        return context

    def get_class_students(self):
        classroom_id = self.kwargs.get('pk')
        if classroom_id:
            classroom = get_object_or_404(Classroom, pk=classroom_id, school=self.request.user.school)
            return classroom.child.all()
        return User.objects.none()
