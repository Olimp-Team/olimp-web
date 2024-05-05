from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.utils.translation import gettext as _
from excel_response import ExcelResponse
from main.models import Register_admin


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
