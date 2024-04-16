from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import View
from excel_response import ExcelResponse
from main.models import *
from .decorators import *
from .models import Register, Register_admin
from .forms import ResultCreateFrom
from django.views.generic import *


class HomePage(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        context = {
            'user': User.objects.filter(id=request.user.id)
        }
        return render(request, 'homepage/homepage.html')


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
            return render(request, 'add_students/add_students.html')
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


class Result(View, LoginRequiredMixin):
    def get(self, request):
        context = {
            'form': form,
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


class ExcelClassroom(View, LoginRequiredMixin):
    def get(self, request, Classroom_id):
        if request.user.is_admin:
            queryset = Register_admin.objects.filter(
                child_admin__classroom__id=Classroom_id)

            data_classroom = [
                [_("№"), _("Фамилия"), _("Имя"), _("Отчество"), _("Пол"), _("Дата рождения (формат 01.08.98)"),
                 _("Статус наличия гражданства"), _("Участник с ОВЗ"), _("Краткое наименование ОУ"),
                 _("Класс, в котором учится участник"), _("Буква класса, в котором учится участник"),
                 _("Английский язык (4, 5-6, 7-8, 9-11)"),
                 _("География (5, 6, 7, 8, 9, 10-11)"),
                 _("Информатика (3, 4)"), _("Искусство (МХК) (5, 6, 7, 8, 9, 10, 11)"),
                 _("История (5, 6, 7, 8, 9, 10-11)"),
                 _("Литература (5, 6, 7, 8, 9, 10, 11)"), _("Музыка (5, 6, 7, 8)"),
                 _("Немецкий язык (4, 5-6, 7-8, 9-11)"),
                 _("Обществознание (5, 6, 7, 8, 9, 10, 11 )"), _("ОБЖ (5, 6, 7, 8, 9, 10-11)"),
                 _("Право (9, 10, 11)"), _("Психология (7-11)"), _("Русский язык (5, 6, 7, 8, 9, 10, 11)"),
                 _("Технология (5-6, 7-8, 9, 10-11)"), _("Физика (5, 6)"),
                 _("Физическая культура (5-6, 7-8, 9-11)"), _("Французский язык (4, 5-6, 7-8, 9-11)"),
                 _("Экология (7, 8, 9, 10, 11)"), _("Экономика (7-9, 10-11)"), _("НШ: литературное чтение (4)"),
                 _("НШ: окружающий мир (4)"), _("НШ: окружающий мир (4)"), _("НШ: русский язык (4)"),
                 _("Кол-во заявлений"),
                 ],

            ]

            for obj in queryset:
                data_classroom.append([
                    obj.child_admin.id,
                    obj.child_admin.last_name,
                    obj.child_admin.first_name,
                    obj.child_admin.surname,
                    obj.child_admin.gender,
                    obj.child_admin.birth_date,
                    'РФ',
                    '',
                    'МАОУ «МЛ № 1»',
                    obj.child_admin.classroom.number,
                    obj.child_admin.classroom.letter,
                    '1' if obj.Olympiad_admin.subject.name == 'Английский язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'География' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Информатика' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Искусство (МХК)' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'История' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Литература' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Музыка' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Немецкий язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Обществознание' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'ОБЖ' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Право' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Психология' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Русский язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Технология' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Физика' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Физическая культура' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Французский язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Экология' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Экономика' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: литературное чтение' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: окружающий мир (4)' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: окружающий мир (4)' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: русский язык (4)' else '0',

                ])

                return ExcelResponse(data_classroom, f'register_classroom')
            else:
                return HttpResponseForbidden()


class ExcelAll(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            queryset = Register_admin.objects.all()  # Получаем данные из нашей модели
            data_all = [
                [_("№"), _("Фамилия"), _("Имя"), _("Отчество"), _("Пол"), _("Дата рождения (формат 01.08.98)"),
                 _("Статус наличия гражданства"), _("Участник с ОВЗ"), _("Краткое наименование ОУ"),
                 _("Класс, в котором учится участник"), _("Буква класса, в котором учится участник"),
                 _("Английский язык (4, 5-6, 7-8, 9-11)"),
                 _("География (5, 6, 7, 8, 9, 10-11)"),
                 _("Информатика (3, 4)"), _("Искусство (МХК) (5, 6, 7, 8, 9, 10, 11)"),
                 _("История (5, 6, 7, 8, 9, 10-11)"),
                 _("Литература (5, 6, 7, 8, 9, 10, 11)"), _("Музыка (5, 6, 7, 8)"),
                 _("Немецкий язык (4, 5-6, 7-8, 9-11)"),
                 _("Обществознание (5, 6, 7, 8, 9, 10, 11 )"), _("ОБЖ (5, 6, 7, 8, 9, 10-11)"),
                 _("Право (9, 10, 11)"), _("Психология (7-11)"), _("Русский язык (5, 6, 7, 8, 9, 10, 11)"),
                 _("Технология (5-6, 7-8, 9, 10-11)"), _("Физика (5, 6)"),
                 _("Физическая культура (5-6, 7-8, 9-11)"), _("Французский язык (4, 5-6, 7-8, 9-11)"),
                 _("Экология (7, 8, 9, 10, 11)"), _("Экономика (7-9, 10-11)"), _("НШ: литературное чтение (4)"),
                 _("НШ: окружающий мир (4)"), _("НШ: окружающий мир (4)"), _("НШ: русский язык (4)"),
                 _("Кол-во заявлений"), ],
                # Заголовки столбцов
            ]
            for obj in queryset:
                data_all.append([
                    obj.child_admin.id,
                    obj.child_admin.last_name,
                    obj.child_admin.first_name,
                    obj.child_admin.surname,
                    obj.child_admin.gender,
                    obj.child_admin.birth_date,
                    'РФ',
                    '',
                    'МАОУ «МЛ № 1»',
                    obj.child_admin.classroom.number,
                    obj.child_admin.classroom.letter,
                    '1' if obj.Olympiad_admin.subject.name == 'Английский язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'География' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Информатика' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Искусство (МХК)' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'История' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Литература' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Музыка' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Немецкий язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Обществознание' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'ОБЖ' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Право' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Психология' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Русский язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Технология' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Физика' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Физическая культура' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Французский язык' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Экология' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'Экономика' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: литературное чтение' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: окружающий мир (4)' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: окружающий мир (4)' else '0',
                    '1' if obj.Olympiad_admin.subject.name == 'НШ: русский язык (4)' else '0',

                ])

            return ExcelResponse(data_all, 'register_all')  # - имя файла Excel
        else:
            return HttpResponseForbidden()
