from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.utils.translation import gettext as _
from excel_response import ExcelResponse
from main.models import Register_admin, Classroom, Subject, Post
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from users.models import User
import pandas as pd


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

            student_data = {}

            for obj in queryset:
                student_id = obj.child_admin.id
                if student_id not in student_data:
                    student_data[student_id] = {
                        "last_name": obj.child_admin.last_name,
                        "first_name": obj.child_admin.first_name,
                        "surname": obj.child_admin.surname,
                        "gender": obj.child_admin.gender,
                        "birth_date": obj.child_admin.birth_date,
                        "class_number": obj.child_admin.classroom.number,
                        "class_letter": obj.child_admin.classroom.letter,
                        "subjects": {
                            "Английский язык": 0,
                            "География": 0,
                            "Информатика": 0,
                            "Искусство (МХК)": 0,
                            "История": 0,
                            "Литература": 0,
                            "Музыка": 0,
                            "Немецкий язык": 0,
                            "Обществознание": 0,
                            "ОБЖ": 0,
                            "Право": 0,
                            "Психология": 0,
                            "Русский язык": 0,
                            "Технология": 0,
                            "Физика": 0,
                            "Физическая культура": 0,
                            "Французский язык": 0,
                            "Экология": 0,
                            "Экономика": 0,
                            "НШ: литературное чтение": 0,
                            "НШ: окружающий мир (4)": 0,
                            "НШ: русский язык (4)": 0,
                        }
                    }

                student_data[student_id]["subjects"][obj.Olympiad_admin.subject.name] = 1

            for student_id, student_info in student_data.items():
                subjects = student_info["subjects"]
                data_classroom.append([
                    student_id,
                    student_info["last_name"],
                    student_info["first_name"],
                    student_info["surname"],
                    student_info["gender"],
                    student_info["birth_date"],
                    'РФ',
                    '',
                    'МАОУ «МЛ № 1»',
                    student_info["class_number"],
                    student_info["class_letter"],
                    subjects["Английский язык"],
                    subjects["География"],
                    subjects["Информатика"],
                    subjects["Искусство (МХК)"],
                    subjects["История"],
                    subjects["Литература"],
                    subjects["Музыка"],
                    subjects["Немецкий язык"],
                    subjects["Обществознание"],
                    subjects["ОБЖ"],
                    subjects["Право"],
                    subjects["Психология"],
                    subjects["Русский язык"],
                    subjects["Технология"],
                    subjects["Физика"],
                    subjects["Физическая культура"],
                    subjects["Французский язык"],
                    subjects["Экология"],
                    subjects["Экономика"],
                    subjects["НШ: литературное чтение"],
                    subjects["НШ: окружающий мир (4)"],
                    subjects["НШ: русский язык (4)"],
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

            student_data = {}

            for obj in queryset:
                student_id = obj.child_admin.id
                if student_id not in student_data:
                    student_data[student_id] = {
                        "last_name": obj.child_admin.last_name,
                        "first_name": obj.child_admin.first_name,
                        "surname": obj.child_admin.surname,
                        "gender": obj.child_admin.gender,
                        "birth_date": obj.child_admin.birth_date,
                        "class_number": obj.child_admin.classroom.number,
                        "class_letter": obj.child_admin.classroom.letter,
                        "subjects": {
                            "Английский язык": 0,
                            "География": 0,
                            "Информатика": 0,
                            "Искусство (МХК)": 0,
                            "История": 0,
                            "Литература": 0,
                            "Музыка": 0,
                            "Немецкий язык": 0,
                            "Обществознание": 0,
                            "ОБЖ": 0,
                            "Право": 0,
                            "Психология": 0,
                            "Русский язык": 0,
                            "Технология": 0,
                            "Физика": 0,
                            "Физическая культура": 0,
                            "Французский язык": 0,
                            "Экология": 0,
                            "Экономика": 0,
                            "НШ: литературное чтение": 0,
                            "НШ: окружающий мир (4)": 0,
                            "НШ: русский язык (4)": 0,
                        }
                    }

                student_data[student_id]["subjects"][obj.Olympiad_admin.subject.name] = 1

            for student_id, student_info in student_data.items():
                subjects = student_info["subjects"]
                data_all.append([
                    student_id,
                    student_info["last_name"],
                    student_info["first_name"],
                    student_info["surname"],
                    student_info["gender"],
                    student_info["birth_date"],
                    'РФ',
                    '',
                    'МАОУ «МЛ № 1»',
                    student_info["class_number"],
                    student_info["class_letter"],
                    subjects["Английский язык"],
                    subjects["География"],
                    subjects["Информатика"],
                    subjects["Искусство (МХК)"],
                    subjects["История"],
                    subjects["Литература"],
                    subjects["Музыка"],
                    subjects["Немецкий язык"],
                    subjects["Обществознание"],
                    subjects["ОБЖ"],
                    subjects["Право"],
                    subjects["Психология"],
                    subjects["Русский язык"],
                    subjects["Технология"],
                    subjects["Физика"],
                    subjects["Физическая культура"],
                    subjects["Французский язык"],
                    subjects["Экология"],
                    subjects["Экономика"],
                    subjects["НШ: литературное чтение"],
                    subjects["НШ: окружающий мир (4)"],
                    subjects["НШ: русский язык (4)"],
                ])

            return ExcelResponse(data_all, 'register_all')  # Имя файла Excel
        else:
            return HttpResponseForbidden()


def import_users(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            import_data(file)
            return redirect('docs:success_import')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def import_data(file):
    df = pd.read_excel(file)

    for index, row in df.iterrows():
        if row['имя_пользователя'] == "имя_пользователя":  # Пропускаем заголовок
            continue

        user, created = User.objects.update_or_create(
            username=row['имя_пользователя'],
            defaults={
                'first_name': row['имя'],
                'last_name': row['фамилия'],
                'surname': row['отчество'],
                'email': row['почта'],
                'birth_date': row['дата_рождения'],
                'gender': row['пол'],
                'is_teacher': row['учитель'] == 1,
                'is_child': row['ученик'] == 1,
                'is_admin': row['администратор'] == 1,
            }
        )

        if created and 'пароль' in row and pd.notna(row['пароль']):
            user.set_password(row['пароль'])
            user.save()

        if pd.notna(row['классное_руководство']):  # классное_руководство
            try:
                number, letter = parse_classroom(row['классное_руководство'])
                classroom_guide = Classroom.objects.get(number=number, letter=letter)
                user.classroom_guide = classroom_guide
            except Classroom.DoesNotExist:
                pass  # Если класс не найден, пропускаем
            user.save()

        if pd.notna(row['класс']):  # класс
            try:
                number, letter = parse_classroom(row['класс'])
                classroom = Classroom.objects.get(number=number, letter=letter)
                user.classroom = classroom
            except Classroom.DoesNotExist:
                pass  # Если класс не найден, пропускаем
            user.save()

        if pd.notna(row['предметы']):  # предметы
            subjects = row['предметы'].split(',')
            for subject in subjects:
                try:
                    subject_obj = Subject.objects.get(name=subject.strip())
                    user.subject.add(subject_obj)
                except Subject.DoesNotExist:
                    pass  # Если предмет не найден, пропускаем

        if pd.notna(row['должности']):  # должности
            posts = row['должности'].split(',')
            for post in posts:
                try:
                    post_obj = Post.objects.get(name=post.strip())
                    user.post_job_teacher.add(post_obj)
                except Post.DoesNotExist:
                    pass  # Если должность не найдена, пропускаем


def parse_classroom(classroom_str):
    number = int(''.join(filter(str.isdigit, classroom_str)))
    letter = ''.join(filter(str.isalpha, classroom_str))
    return number, letter
