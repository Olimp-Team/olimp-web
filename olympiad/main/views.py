from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import View
from excel_response import ExcelResponse

from main.models import *
from .decorators import *


# Страницы учеников
@login_required
def home(request):
    return render(request, 'homepage/homepage.html')


@login_required
@is_child
def register_olympiad(request):
    context = {
        'olympiads': Olympiad.objects.filter(class_olympiad=request.user.classroom.number),
        'olympiads_last': Olympiad.objects.filter(class_olympiad=request.user.classroom.number).last()
    }
    return render(request, 'register-olympiad/register-olympiad.html', context)


@login_required
@is_child
def register_add(request, Olympiad_id):
    olympiad = Olympiad.objects.get(id=Olympiad_id)
    registers = Register.objects.filter(child=request.user, Olympiad=olympiad)
    if not registers.exists():
        Register.objects.create(child=request.user, Olympiad=olympiad, teacher=request.user.classroom.teacher)
    else:
        basket = registers.first()
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@is_child
def register_remove(request, Register_id):
    register_basket = Register.objects.get(id=Register_id)
    register_basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@is_child
def basket_student_applications(request):
    context = {
        'register': Register.objects.filter(child=request.user, status_send=False)
    }
    return render(request, 'basket-student-applications/basket-student-applications.html', context)


@login_required
@is_child
def register_send(request):
    reg_create = Register_send.objects.create(
        Register_send_str=Register.objects.get(child=request.user, status_send=False))
    Register.objects.filter(child=request.user).update(status_send=True)
    reg_create.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Страницы учителей
@login_required
@is_teacher
def student_applications(request):
    reg = Register_send.objects.filter(Register_send_str__child__classroom__exact=request.user.classroom_guide,
                                       status_teacher=False)
    context = {
        'register': reg
    }
    return render(request, 'student-applications/student-applications.html', context)


@login_required
@is_teacher
def register_remove_teacher(request, Register_id):
    register_basket = Register_send.objects.get(id=Register_id)
    register_basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@is_teacher
def register_send_teacher(request):
    reg_create_teacher = Register_admin.objects.create(Register_admin_str=Register_send.objects.get(
        Register_send_str__child__classroom__exact=request.user.classroom_guide, status_teacher=False))

    Register_send.objects.filter(Register_send_str__child__classroom__teacher=request.user).update(status_teacher=True)
    reg_create_teacher.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Страницы администратора
@login_required
@is_admin
def register_list_classroom(request):
    context = {
        'register': Register_admin.objects.all()
    }
    return render(request, 'applications-from-classroom-teachers/applications-from-classroom-teachers.html', context)


@login_required
@is_admin
def child_remove_admin(request, User_id):
    user_id = User.objects.get(id=User_id)
    user_id.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def student_applications_admin(request, Classroom_id):
    classroom = Classroom.objects.get(id=Classroom_id)
    classroom_children = User.objects.filter(classroom_id=Classroom_id)
    context = {
        'classroom': classroom,
        'child': classroom_children
    }
    return render(request, 'student_applications_admin/student_applications_admin.html', context)


@login_required
@is_admin
def list_classroom(request):
    context = {
        'classroom': Classroom.objects.all(),
    }
    return render(request, 'list_classroom/list_classroom.html', context)


def excel_classroom(request, Classroom_id):
    queryset = Register_admin.objects.filter(
        Register_admin_str__Register_send_str__child__classroom__id=Classroom_id)

    data_classroom = [
        [_("№"), _("Фамилия"), _("Имя"), _("Отчество"), _("Пол"), _("Дата рождения (формат 01.08.98)"),
         _("Статус наличия гражданства"), _("Участник с ОВЗ"), _("Краткое наименование ОУ"),
         _("Класс, в котором учится участник"), _("Буква класса, в котором учится участник"),
         _("Английский язык (4, 5-6, 7-8, 9-11)"),
         _("География (5, 6, 7, 8, 9, 10-11)"),
         _("Информатика (3, 4)"), _("Искусство (МХК) (5, 6, 7, 8, 9, 10, 11)"), _("История (5, 6, 7, 8, 9, 10-11)"),
         _("Литература (5, 6, 7, 8, 9, 10, 11)"), _("Музыка (5, 6, 7, 8)"), _("Немецкий язык (4, 5-6, 7-8, 9-11)"),
         _("Обществознание (5, 6, 7, 8, 9, 10, 11 )"), _("ОБЖ (5, 6, 7, 8, 9, 10-11)"),
         _("Право (9, 10, 11)"), _("Психология (7-11)"), _("Русский язык (5, 6, 7, 8, 9, 10, 11)"),
         _("Технология (5-6, 7-8, 9, 10-11)"), _("Физика (5, 6)"),
         _("Физическая культура (5-6, 7-8, 9-11)"), _("Французский язык (4, 5-6, 7-8, 9-11)"),
         _("Экология (7, 8, 9, 10, 11)"), _("Экономика (7-9, 10-11)"), _("НШ: литературное чтение (4)"),
         _("НШ: окружающий мир (4)"), _("НШ: окружающий мир (4)"), _("НШ: русский язык (4)"), _("Кол-во заявлений"),
         ],

    ]

    for obj in queryset:
        data_classroom.append([
            obj.Register_admin_str.Register_send_str.child.id,
            obj.Register_admin_str.Register_send_str.child.last_name,
            obj.Register_admin_str.Register_send_str.child.first_name,
            obj.Register_admin_str.Register_send_str.child.surname,
            obj.Register_admin_str.Register_send_str.child.gender,
            obj.Register_admin_str.Register_send_str.child.birth_date,
            'РФ',
            '',
            'МАОУ «МЛ № 1»',
            obj.Register_admin_str.Register_send_str.child.classroom.number,
            obj.Register_admin_str.Register_send_str.child.classroom.letter,
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Английский язык' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'География' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Информатика' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Искусство (МХК)' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'История' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Литература' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Музыка' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Немецкий язык' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Обществознание' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'ОБЖ' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Право' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Психология' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Русский язык' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Технология' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Физика' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Физическая культура' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Французский язык' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Экология' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Экономика' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: литературное чтение' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: окружающий мир (4)' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: окружающий мир (4)' else '0',
            '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: русский язык (4)' else '0',

        ])

        return ExcelResponse(data_classroom, f'register_classroom')


class ExportToExcelView(View):
    def get(self, request):
        queryset = Register_admin.objects.all()  # Получаем данные из нашей модели
        data_all = [
            [_("№"), _("Фамилия"), _("Имя"), _("Отчество"), _("Пол"), _("Дата рождения (формат 01.08.98)"),
             _("Статус наличия гражданства"), _("Участник с ОВЗ"), _("Краткое наименование ОУ"),
             _("Класс, в котором учится участник"), _("Буква класса, в котором учится участник"),
             _("Английский язык (4, 5-6, 7-8, 9-11)"),
             _("География (5, 6, 7, 8, 9, 10-11)"),
             _("Информатика (3, 4)"), _("Искусство (МХК) (5, 6, 7, 8, 9, 10, 11)"), _("История (5, 6, 7, 8, 9, 10-11)"),
             _("Литература (5, 6, 7, 8, 9, 10, 11)"), _("Музыка (5, 6, 7, 8)"), _("Немецкий язык (4, 5-6, 7-8, 9-11)"),
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
                obj.Register_admin_str.Register_send_str.child.id,
                obj.Register_admin_str.Register_send_str.child.last_name,
                obj.Register_admin_str.Register_send_str.child.first_name,
                obj.Register_admin_str.Register_send_str.child.surname,
                obj.Register_admin_str.Register_send_str.child.gender,
                obj.Register_admin_str.Register_send_str.child.birth_date,
                'РФ',
                '',
                'МАОУ «МЛ № 1»',
                obj.Register_admin_str.Register_send_str.child.classroom.number,
                obj.Register_admin_str.Register_send_str.child.classroom.letter,
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Английский язык' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'География' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Информатика' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Искусство (МХК)' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'История' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Литература' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Музыка' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Немецкий язык' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Обществознание' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'ОБЖ' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Право' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Психология' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Русский язык' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Технология' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Физика' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Физическая культура' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Французский язык' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Экология' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'Экономика' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: литературное чтение' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: окружающий мир (4)' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: окружающий мир (4)' else '0',
                '1' if obj.Register_admin_str.Register_send_str.Olympiad.subject.name == 'НШ: русский язык (4)' else '0',

            ])

        return ExcelResponse(data_all, 'register_all')  # - имя файла Excel
