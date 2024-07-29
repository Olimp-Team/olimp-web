from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from school.models import School
from classroom.models import Classroom
from register.models import Register_admin, Register_send
from main.models import Olympiad, Subject, categories, Level_olympiad, Stage
from docs.views import import_data, parse_classroom
import pandas as pd
from io import BytesIO


class DocsViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.school = School.objects.create(name="Test School")
        self.admin = User.objects.create_user(username="admin1", password="adminpass", is_admin=True, school=self.school)
        self.teacher = User.objects.create_user(username="teacher1", password="teacherpass", is_teacher=True, school=self.school)
        self.child = User.objects.create_user(username="child1", password="childpass", is_child=True, school=self.school)
        self.classroom = Classroom.objects.create(number=1, letter='A', teacher=self.teacher, school=self.school)
        self.classroom.child.add(self.child)
        self.subject = Subject.objects.create(name="Math")
        self.olympiad = Olympiad.objects.create(name="Test Olympiad", subject=self.subject)
        self.register_admin = Register_admin.objects.create(child_admin=self.child, Olympiad_admin=self.olympiad, school=self.school)
        self.register_send = Register_send.objects.create(child_send=self.child, Olympiad_send=self.olympiad, school=self.school)

    def test_excel_classroom(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:excel_classroom', args=[self.classroom.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="Zayvki 1A classa.xlsx"')

    def test_excel_all(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:excel_all'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="Baza {self.school.name}.xlsx"')

    def test_import_users_view(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:import_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

        data = {
            'имя_пользователя': 'newuser1',
            'имя': 'First',
            'фамилия': 'Last',
            'отчество': 'Surname',
            'почта': 'test@example.com',
            'дата_рождения': '2000-01-01',
            'пол': 'М',
            'учитель': 0,
            'ученик': 1,
            'администратор': 0,
            'класс': '1A',
            'предметы': 'Math',
            'должности': '',
            'пароль': 'password'
        }
        file = BytesIO()
        df = pd.DataFrame([data])
        df.to_excel(file, index=False)
        file.seek(0)

        response = self.client.post(reverse('docs:import_users'), {'file': file})
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_export_excel_view(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:export_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=results.xlsx')

    def test_create_zip_archive(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:create_zip_archive'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="applications.zip"')

    def test_create_zip_archive_for_teacher(self):
        self.client.login(username='teacher1', password='teacherpass')
        response = self.client.get(reverse('docs:create_zip_archive_for_teacher'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="applications.zip"')

    def test_import_olympiads_view(self):
        self.client.login(username='admin1', password='adminpass')
        response = self.client.get(reverse('docs:import_olympiads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'import_olympiads.html')

        data = {
            'Категория олимпиады': 'Category',
            'Название уровня': 'Level',
            'Название этапа': 'Stage',
            'Название школьного предмета': 'Math',
            'Название олимпиады': 'Test Olympiad',
            'Описание олимпиады': 'Description',
            'Класс олимпиады': '1A'
        }
        file = BytesIO()
        df = pd.DataFrame([data])
        df.to_excel(file, index=False)
        file.seek(0)

        response = self.client.post(reverse('docs:import_olympiads'), {'file': file})
        self.assertEqual(response.status_code, 302)

    def test_import_data_function(self):
        data = {
            'имя_пользователя': 'newuser1',
            'имя': 'First',
            'фамилия': 'Last',
            'отчество': 'Surname',
            'почта': 'test@example.com',
            'дата_рождения': '2000-01-01',
            'пол': 'М',
            'учитель': 0,
            'ученик': 1,
            'администратор': 0,
            'класс': '1A',
            'предметы': 'Math',
            'должности': '',
            'пароль': 'password'
        }
        file = BytesIO()
        df = pd.DataFrame([data])
        df.to_excel(file, index=False)
        file.seek(0)

        import_data(file, self.school)
        self.assertTrue(User.objects.filter(username='newuser1').exists())

    def test_parse_classroom_function(self):
        number, letter = parse_classroom('1A')
        self.assertEqual(number, '1')
        self.assertEqual(letter, 'A')
