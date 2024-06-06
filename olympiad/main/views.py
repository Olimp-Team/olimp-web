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
from .models import Register_admin
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

class RegisterPage(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_child:
            context = {
                'olympiads': Olympiad.objects.filter(class_olympiad=request.user.classroom.number),
                'olympiads_last': Olympiad.objects.filter(class_olympiad=request.user.classroom.number).last()
            }
            return render(request, 'register-olympiad/register-olympiad.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if request.user.is_child:
            pass
        else:
            return HttpResponseForbidden()


class RegisterAdd(View, LoginRequiredMixin):
    def get(self, request, Olympiad_id):
        if request.user.is_child:
            olympiad = Olympiad.objects.get(id=Olympiad_id)
            # Проверка наличия существующей записи и создание новой, если не существует
            register, created = Register.objects.get_or_create(
                child=request.user,
                Olympiad=olympiad,
                defaults={'teacher': request.user.classroom.teacher}
            )
            # Если заявка уже существует, то можно выполнить другие действия, если это необходимо
            if not created:
                register.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request):
        return HttpResponseForbidden()


class RegisterDelete(View, LoginRequiredMixin):
    def get(self, request, Register_id):
        if request.user.is_child:
            register_basket = Register.objects.get(id=Register_id)
            register_basket.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class BasketStudentApp(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_child:
            context = {
                'register': Register.objects.filter(child=request.user, status_send=False)
            }
            return render(request, 'basket-student-applications/basket-student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class RegisterSend(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_child:
            objs = [
                Register_send(
                    teacher_send=i.teacher,
                    child_send=i.child,
                    Olympiad_send=i.Olympiad,
                )
                for i in Register.objects.filter(child=request.user, status_send=False)
            ]

            Register_send.objects.bulk_create(objs)
            Register.objects.filter(child=request.user).update(status_send=True)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


########################################################################################################################
# Страницы учителей
class StudentApp(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            # Получаем все заявки учеников, которые связаны с классом текущего учителя
            reg = Register_send.objects.filter(
                teacher_send__classroom_guide=request.user.classroom_guide,
                status_send=False
            )

            # Создаем словарь, где ключом будет ученик, а значением - список олимпиад
            student_olympiads = {}
            for register in reg:
                if register.child_send not in student_olympiads:
                    student_olympiads[register.child_send] = []
                student_olympiads[register.child_send].append(register.Olympiad_send)

            context = {
                'student_olympiads': student_olympiads
            }
            return render(request, 'student-applications/student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        return HttpResponseForbidden()


# class RegisterRemoveTeacher(View, LoginRequiredMixin):
#     def get(self, request):
#         if request.user.is_teacher:
#             reg = Register_send.objects.filter(teacher_send__classroom_guide=request.user.classroom_guide,
#                                                status_teacher=False)
#             context = {
#                 'register': reg
#             }
#             return render(request, 'student-applications/student-applications.html', context)
#         else:
#             return HttpResponseForbidden()
#
#     def post(self, request, *args, **kwargs):
#         pass
class RegisterDeleteTeacher(View, LoginRequiredMixin):
    def post(self, request, Olympiad_id, student_id):
        if request.user.is_teacher:
            try:
                register = Register_send.objects.get(Olympiad_send_id=Olympiad_id, child_send_id=student_id,
                                                     is_deleted=False)
                register.is_deleted = True
                register.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except Register_send.DoesNotExist:
                return HttpResponseForbidden("Заявка не найдена.")
        else:
            return HttpResponseForbidden()


# class RegisterSendTeacher(View, LoginRequiredMixin):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_teacher:
#             RST = [
#                 Register_admin(
#                     teacher_admin=i.teacher_send,
#                     child_admin=i.child_send,
#                     Olympiad_admin=i.Olympiad_send,
#
#                 )
#                 for i in
#                 Register_send.objects.filter(child_send__classroom__exact=request.user.classroom_guide,
#                                              status_teacher=False)
#             ]
#             Register_admin.objects.bulk_create(RST)
#             Register_send.objects.filter(child_send__classroom__teacher=request.user).update(status_teacher=True)
#
#             return HttpResponseRedirect(request.META['HTTP_REFERER'])
#         else:
#             return HttpResponseForbidden()
# class RegisterSendTeacher(View, LoginRequiredMixin):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_teacher:
#             registers = Register_send.objects.filter(
#                 child_send__classroom=request.user.classroom_guide,
#                 status_teacher=False
#             )
#             for register in registers:
#                 # Обновляем существующую запись или создаем новую, если не существует
#                 Register_admin.objects.update_or_create(
#                     teacher_admin=register.teacher_send,
#                     child_admin=register.child_send,
#                     Olympiad_admin=register.Olympiad_send,
#                     defaults={'status_admin': False}
#                 )
#             # Обновляем статус заявок в Register_send
#             registers.update(status_teacher=True)
#
#             return HttpResponseRedirect(request.META['HTTP_REFERER'])
#         else:
#             return HttpResponseForbidden()

class RegisterSendTeacher(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            # Получаем заявки от текущего учителя, которые ещё не были обработаны
            registers = Register_send.objects.filter(
                teacher_send=request.user,
                status_send=False
            )
            for register in registers:
                # Обновляем существующую запись или создаем новую, если не существует
                Register_admin.objects.update_or_create(
                    teacher_admin=register.teacher_send,
                    child_admin=register.child_send,
                    Olympiad_admin=register.Olympiad_send,
                    defaults={'status_teacher': True, 'status_admin': False}
                )
            # Обновляем статус заявок в Register
            registers.update(status_send=True)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


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


# class RegisterListClassroom(View, LoginRequiredMixin):
#     def get(self, request):
#         if request.user.is_admin:
#             context = {
#                 'register': Register_admin.objects.all()
#             }
#             return render(request, 'applications-from-classroom-teachers/applications-from-classroom-teachers.html', context)
#         else:
#             return HttpResponseForbidden()

class RegisterListClassroom(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            # Получаем все заявки и группируем их по учебным классам
            registers = Register_admin.objects.all()
            grouped_registers = {}
            for register in registers:
                classroom = register.child_admin.classroom  # Предполагаем, что у модели child_admin есть поле classroom
                if classroom not in grouped_registers:
                    grouped_registers[classroom] = []
                grouped_registers[classroom].append(register)

            context = {
                'grouped_registers': grouped_registers
            }
            return render(request, 'applications-from-classroom-teachers/applications-from-classroom-teachers.html',
                          context)
        else:
            return HttpResponseForbidden()


class ChildRemoveAdmin(View, LoginRequiredMixin):
    def get(self, request, User_id):
        user_id = User.objects.get(id=User_id)
        user_id.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class StudentAdminApp(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request, Classroom_id):
        classroom = Classroom.objects.get(id=Classroom_id)
        classroom_children = User.objects.filter(classroom_id=Classroom_id)
        context = {
            'classroom': classroom,
            'child': classroom_children
        }
        return render(request, 'student_applications_admin/student_applications_admin.html', context)

    def post(self, request):
        pass


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


class CreateAdmin(View, LoginRequiredMixin, AdminRequiredMixin):
    def get(self, request):
        return render(request, 'add_admin/add_admin.html')


# class CreateChildView(CreateView, LoginRequiredMixin):
#     form_class = NewChildForm
#     template_name = 'add_students/add_students.html'
#     success_url = reverse_lazy('main:list_classroom')
#
#     def form_valid(self, form):
#         classroom = form.cleaned_data['classroom']
#         form.save()
#         return super().form_valid(form)


class CreateChild(View, LoginRequiredMixin, AdminRequiredMixin):
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
        form = NewTeacherForm()
        context = {'form': form}
        return render(request, 'add_teacher/add_teacher.html', context)

    def post(self, request):
        form = NewTeacherForm(data=request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.save()
            classroom_guide = form.cleaned_data['classroom_guide']
            Classroom.objects.get(id=classroom_guide.id).teacher.add(teacher)
            return HttpResponseRedirect(reverse('main:list_classroom'))
        context = {'form': form}
        return render(request, 'add_students/add_students.html', context)


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
