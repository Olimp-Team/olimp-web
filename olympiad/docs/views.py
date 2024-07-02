import os
import pymorphy3
import zipfile
import tempfile
import pandas as pd
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import View, ListView
from django.utils.translation import gettext as _
from excel_response import ExcelResponse
from main.models import *
from register.models import *
from result.models import *
from users.models import *
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from django.db.models import Q
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from users.mixins import AdminRequiredMixin
from django.http import HttpResponse


class ExcelClassroom(AdminRequiredMixin, View):
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


class ExcelAll(AdminRequiredMixin, View):
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


class import_users(View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            self.import_data(file)  # Вызов статического метода
            return redirect('docs:succes_import')

    @staticmethod
    def import_data(file):
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            if row['имя_пользователя'] == "имя_пользователя":  # Пропускаем заголовок
                continue

            # Проверка на наличие почты
            if pd.notna(row['почта']):
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


class parse_classroom():
    def post(self, classroom_str):
        number = int(''.join(filter(str.isdigit, classroom_str)))
        letter = ''.join(filter(str.isalpha, classroom_str))
        return number, letter


class DashboardView(AdminRequiredMixin, ListView):
    model = Result
    template_name = 'dashboard.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтры
        start_date = self.request.GET.get('start-date')
        end_date = self.request.GET.get('end-date')
        class_filter = self.request.GET.get('class')
        subject_filter = self.request.GET.get('subject')
        student_filter = self.request.GET.get('student')
        olympiad_filter = self.request.GET.get('olympiad')

        if start_date and end_date:
            queryset = queryset.filter(date_added__range=[start_date, end_date])
        if class_filter:
            queryset = queryset.filter(info_children__classroom__id=class_filter)
        if subject_filter:
            queryset = queryset.filter(info_olympiad__subject__id=subject_filter)
        if student_filter:
            queryset = queryset.filter(
                Q(info_children__first_name__icontains=student_filter) |
                Q(info_children__last_name__icontains=student_filter) |
                Q(info_children__surname__icontains=student_filter)
            )
        if olympiad_filter:
            queryset = queryset.filter(info_olympiad__id=olympiad_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classrooms'] = Classroom.objects.all()
        context['subjects'] = Subject.objects.all()
        context['olympiads'] = Olympiad.objects.all()
        return context


class ExportExcelView(AdminRequiredMixin, ListView):
    model = Result

    def get_queryset(self):
        queryset = Result.objects.all()

        # Фильтры
        start_date = self.request.GET.get('start-date')
        end_date = self.request.GET.get('end-date')
        class_filter = self.request.GET.get('class')
        subject_filter = self.request.GET.get('subject')
        student_filter = self.request.GET.get('student')
        olympiad_filter = self.request.GET.get('olympiad')

        if start_date and end_date:
            queryset = queryset.filter(date_added__date__range=[start_date, end_date])
        if class_filter:
            queryset = queryset.filter(info_children__classroom__id=class_filter)
        if subject_filter:
            queryset = queryset.filter(info_olympiad__subject__id=subject_filter)
        if student_filter:
            queryset = queryset.filter(
                Q(info_children__first_name__icontains=student_filter) |
                Q(info_children__last_name__icontains=student_filter) |
                Q(info_children__surname__icontains=student_filter)
            )
        if olympiad_filter:
            queryset = queryset.filter(info_olympiad__id=olympiad_filter)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Подготовка данных для выгрузки
        data = []
        for result in queryset:
            data.append([
                result.info_children.get_full_name(),
                result.info_olympiad.name,
                result.info_olympiad.subject.name,
                f"{result.info_children.classroom.number} {result.info_children.classroom.letter}",
                result.points,
                result.get_status_result_display(),
                result.date_added.replace(tzinfo=None)  # Удаление информации о временной зоне
            ])

        # Создание DataFrame
        df = pd.DataFrame(data, columns=[
            'Ученик', 'Олимпиада', 'Предмет', 'Класс', 'Очки', 'Статус', 'Дата'
        ])

        # Создание HttpResponse с заголовками для выгрузки
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        # Сохранение DataFrame в Excel файл
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')

        return response


def create_pdf_for_student(student, olympiads, output_path):
    font_path = os.path.join('static', 'fonts', 'timesnewromanpsmt.ttf')
    pdfmetrics.registerFont(TTFont('timesnewromanpsmt', font_path))

    pdf_canvas = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 50
    x_right = width - margin
    y_top = height - margin

    morph = pymorphy3.MorphAnalyzer()

    def to_accusative(name):
        parsed_name = morph.parse(name)[0]
        return parsed_name.inflect({'accs'}).word.capitalize()

    pdf_canvas.setFont("timesnewromanpsmt", 12)

    subjects_str = ', '.join(olympiads)
    full_name_accusative = f"{to_accusative(student.last_name)} {to_accusative(student.first_name)} {to_accusative(student.surname)}"

    pdf_canvas.drawRightString(x_right, y_top, 'В оргкомитет школьного этапа')
    y_top -= 20
    pdf_canvas.drawRightString(x_right, y_top, 'всероссийской и муниципальной')
    y_top -= 20
    pdf_canvas.drawRightString(x_right, y_top, 'олимпиад школьников')
    y_top -= 20
    pdf_canvas.drawRightString(x_right, y_top, '________________________________')
    y_top -= 20
    pdf_canvas.drawRightString(x_right, y_top, '________________________________')
    y_top -= 20
    pdf_canvas.drawRightString(x_right, y_top, '________________________________')
    pdf_canvas.setFont("timesnewromanpsmt", 10)
    y_top -= 20
    pdf_canvas.drawRightString(x_right, y_top, '(Ф.И.О. родителя (законного представителя))')
    y_top -= 40
    pdf_canvas.setFont("timesnewromanpsmt", 12)
    pdf_canvas.drawCentredString(width / 2.0, y_top, 'Заявление')
    y_top -= 40

    son_or_daughter = 'сына' if student.gender == 'М' else 'дочь'

    pdf_canvas.drawString(margin, y_top, f'Прошу включить моего {son_or_daughter} {full_name_accusative},')
    y_top -= 20
    pdf_canvas.drawString(margin, y_top,
                          f'обучающегося (ся) {student.classroom.number} {student.classroom.letter} класса МАОУ «МЛ № 1» г. Магнитогорска,')
    y_top -= 20
    pdf_canvas.drawString(margin, y_top, 'в состав участников школьного этапа всероссийской и муниципальной')
    y_top -= 20
    pdf_canvas.drawString(margin, y_top, f'олимпиад в 2023-2024 учебном году по следующим предметам:')
    y_top -= 40

    pdf_canvas.drawString(margin, y_top, subjects_str)
    y_top -= 20

    pdf_canvas.drawString(margin, y_top, 'С Порядком проведения всероссийской олимпиады школьников,')
    y_top -= 20
    pdf_canvas.drawString(margin, y_top, 'утвержденным приказом Министерства образования и науки Российской Федерации')
    y_top -= 20
    pdf_canvas.drawString(margin, y_top, 'от 27 ноября 2020г. N678 (ред. от 26.01.2023), ознакомлен(а).')
    y_top -= 40

    pdf_canvas.drawString(margin, y_top,
                          'Дата _______________________________              Подпись _______________________________')
    y_top -= 60

    if y_top < 100:
        pdf_canvas.showPage()
        pdf_canvas.setFont("timesnewromanpsmt", 12)
        y_top = height - margin

    pdf_canvas.save()


class create_zip_archive(View):
    def get(self, request):
        if not request.user.is_admin:
            return HttpResponseForbidden()

        with tempfile.TemporaryDirectory() as temp_dir:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                registers = Register_admin.objects.filter(status_admin=False)
                classes = {}

                for register in registers:
                    student = register.child_admin
                    olympiad = register.Olympiad_admin
                    class_name = f'{student.classroom.number}{student.classroom.letter}'
                    if class_name not in classes:
                        classes[class_name] = {}
                    if student not in classes[class_name]:
                        classes[class_name][student] = []
                    classes[class_name][student].append(olympiad.subject.name)

                for class_name, students in classes.items():
                    class_dir = os.path.join(temp_dir, class_name)
                    os.makedirs(class_dir, exist_ok=True)
                    for student, subjects in students.items():
                        student_file = os.path.join(class_dir, f'{student.last_name}_{student.first_name}.pdf')
                        create_pdf_for_student(student, subjects, student_file)

                with zipfile.ZipFile(temp_zip.name, 'w') as zf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

            with open(temp_zip.name, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="applications.zip"'

            os.remove(temp_zip.name)
            return response


class create_zip_archive_for_teacher(View):
    def post(self, request):
        if not request.user.is_teacher:
            return HttpResponseForbidden()

        with tempfile.TemporaryDirectory() as temp_dir:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
                teacher = request.user
                classroom = teacher.classroom_guide

                # Убедимся, что classroom существует и имеет связанных учеников
                if classroom is None:
                    return HttpResponseBadRequest("Класс не найден для текущего учителя")

                # Найти все заявки учеников класса, которым руководит текущий учитель
                registers = Register_send.objects.filter(
                    child_send__classroom=request.user.classroom_guide,
                )

                classes = {}

                for register in registers:
                    student = register.child_send
                    olympiad = register.Olympiad_send
                    class_name = f'{student.classroom.number}{student.classroom.letter}'
                    if class_name not in classes:
                        classes[class_name] = {}
                    if student not in classes[class_name]:
                        classes[class_name][student] = []
                    classes[class_name][student].append(olympiad.subject.name)

                for class_name, students in classes.items():
                    class_dir = os.path.join(temp_dir, class_name)
                    os.makedirs(class_dir, exist_ok=True)
                    for student, subjects in students.items():
                        student_file = os.path.join(class_dir, f'{student.last_name}_{student.first_name}.pdf')
                        create_pdf_for_student(student, subjects, student_file)

                with zipfile.ZipFile(temp_zip.name, 'w') as zf:
                    for root, _, files in os.walk(temp_dir):
                        for file in files:
                            zf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_dir))

            with open(temp_zip.name, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="applications.zip"'

            os.remove(temp_zip.name)
            return response


class import_olympiads(View):
    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                category, _ = categories.objects.get_or_create(name=row['Категория олимпиады'])
                level, _ = Level_olympiad.objects.get_or_create(name=row['Название уровня'])
                stage, _ = Stage.objects.get_or_create(name=row['Название этапа'])
                subject, _ = Subject.objects.get_or_create(name=row['Название школьного предмета'])
                Olympiad.objects.create(
                    name=row['Название олимпиады'],
                    description=row['Описание олимпиады'],
                    category=category,
                    level=level,
                    stage=stage,
                    subject=subject,
                    class_olympiad=row['Класс олимпиады']
                )
            return HttpResponseRedirect('/success_url/')

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'import_olympiads.html', {'form': form})
