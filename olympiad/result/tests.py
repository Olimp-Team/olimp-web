from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Olympiad, Stage
from register.models import RegisterAdmin
from result.models import Result
from users.models import User, Classroom, School
import io
import pandas as pd


class ResultTests(TestCase):
    def setUp(self):
        # Создаем школу
        self.school = School.objects.create(name='Test School')

        # Создаем пользователей
        self.admin_user = get_user_model().objects.create_user(
            username='admin_user', password='password', is_admin=True, school=self.school)
        self.teacher_user = get_user_model().objects.create_user(
            username='teacher_user', password='password', is_teacher=True, school=self.school)
        self.child_user = get_user_model().objects.create_user(
            username='child_user', password='password', is_child=True, school=self.school)

        # Создаем класс и назначаем ребенка
        self.classroom = Classroom.objects.create(number=5, letter='A', school=self.school, teacher=self.teacher_user)
        self.child_user.classroom = self.classroom
        self.child_user.save()

        # Создаем этапы и олимпиады
        self.stage = Stage.objects.create(name='Школьный')
        self.olympiad = Olympiad.objects.create(
            name='Test Olympiad', stage=self.stage, class_olympiad=5, subject_id=1, level_id=1, category_id=1)

        # Создаем регистрацию администратора
        self.register_admin = RegisterAdmin.objects.create(child_admin=self.child_user, olympiad_admin=self.olympiad)

        # Создаем результаты
        self.result = Result.objects.create(
            info_children=self.child_user, info_olympiad=self.olympiad, points=90, status_result=Result.PARTICIPANT,
            school=self.school)

        # Создаем клиент для тестирования
        self.client = Client()

    def test_result_list_view(self):
        """Тест для проверки списка результатов олимпиад"""
        self.client.login(username='admin_user', password='password')
        response = self.client.get(reverse('result:results_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'result/result.html')

    def test_add_result_view(self):
        """Тест для добавления результата олимпиады"""
        self.client.login(username='admin_user', password='password')
        response = self.client.post(reverse('result:add_result'), {
            'student': self.child_user.id,
            'olympiad': self.olympiad.id,
            'score': 95,
            'status': Result.WINNER
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Result.objects.filter(info_children=self.child_user, info_olympiad=self.olympiad, points=95,
                                              status_result=Result.WINNER).exists())

    def test_export_results_view(self):
        """Тест для экспорта результатов олимпиад"""
        self.client.login(username='admin_user', password='password')
        response = self.client.get(reverse('result:export_results'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=results.xlsx')

    def test_import_results_view(self):
        """Тест для импорта результатов олимпиад"""
        self.client.login(username='admin_user', password='password')
        data = {
            'Фамилия': [self.child_user.last_name],
            'Имя': [self.child_user.first_name],
            'Отчество': [self.child_user.surname],
            'Название олимпиады': [self.olympiad.name],
            'Количество очков': [95],
            'Статус результата': [Result.WINNER]
        }
        df = pd.DataFrame(data)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)

        response = self.client.post(reverse('result:import_results'), {'excel_file': buffer})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Result.objects.filter(info_children=self.child_user, info_olympiad=self.olympiad, points=95,
                                              status_result=Result.WINNER).exists())

    def test_get_olympiads_view(self):
        """Тест для получения списка олимпиад ученика"""
        self.client.login(username='admin_user', password='password')
        response = self.client.get(reverse('result:get_olympiads'), {'student_id': self.child_user.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], self.olympiad.name)

    def test_student_result_list_view(self):
        """Тест для просмотра результатов конкретного ученика"""
        self.client.login(username='child_user', password='password')
        response = self.client.get(reverse('result:student_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_results.html')
        self.assertContains(response, self.olympiad.name)
        self.assertContains(response, 90)

    def test_get_students_view(self):
        """Тест для получения списка учеников класса по AJAX запросу"""
        self.client.login(username='admin_user', password='password')
        response = self.client.get(reverse('result:get_students'), {'classroom_id': self.classroom.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.child_user.get_full_name())
