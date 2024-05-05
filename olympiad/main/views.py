from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import *
from users.forms import NewChildForm
from .decorators import *
from .models import Register, Register_admin
from .forms import ResultCreateFrom
from django.views.generic import *
from users.models import User


def page_not_found(request, exception):
    return HttpResponseNotFound('Sorry, you are not allowed to see this page.')


class HomePage(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'homepage/homepage.html', )


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
            registers = Register.objects.filter(child=request.user, Olympiad=olympiad)
            if not registers.exists():
                Register.objects.create(child=request.user, Olympiad=olympiad, teacher=request.user.classroom.teacher)
            else:
                basket = registers.first()
                basket.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if request.user.is_child:
            pass
        else:
            return HttpResponseForbidden()


class RegisterAdd(View, LoginRequiredMixin):
    def get(self, request, Olympiad_id):
        if request.user.is_child:
            olympiad = Olympiad.objects.get(id=Olympiad_id)
            registers = Register.objects.filter(child=request.user, Olympiad=olympiad)
            if not registers.exists():
                Register.objects.create(child=request.user, Olympiad=olympiad, teacher=request.user.classroom.teacher)
            else:
                basket = registers.first()
                basket.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


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


# Страницы администратора

class ListOlympiad(TemplateView, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            context = {
                'olympiad': Olympiad.objects.filter()
            }
            return render(request, 'list_olympiad/list_olympiad.html', context)
        else:
            return HttpResponseForbidden()


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


class CreateChild(CreateView, LoginRequiredMixin):
    form_class = NewChildForm
    template_name = 'add_students/add_students.html'
    success_url = reverse_lazy('list_classroom')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CreateTeacher(View, LoginRequiredMixin):
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
