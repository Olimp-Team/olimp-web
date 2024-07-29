from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Olympiad, Stage, Category, LevelOlympiad, Subject
from register.models import Register, RegisterSend, Recommendation, RegisterAdmin
from users.models import User, Classroom, School
from django.utils import timezone
import uuid


class RegisterTests(TestCase):

    def setUp(self):
        # Создаем школу
        self.school = School.objects.create(name='Test School')

        # Создаем уникальные имена пользователей
        admin_username = f'admin_{uuid.uuid4()}'
        teacher_username = f'teacher_{uuid.uuid4()}'
        child_username = f'child_{uuid.uuid4()}'

        # Создаем пользователей
        self.admin_user = get_user_model().objects.create_user(
            username=admin_username, password='password', is_admin=True, school=self.school)
        self.teacher_user = get_user_model().objects.create_user(
            username=teacher_username, password='password', is_teacher=True, school=self.school)
        self.child_user = get_user_model().objects.create_user(
            username=child_username, password='password', is_child=True, school=self.school)

        # Создаем класс и назначаем ребенка и учителя
        self.classroom = Classroom.objects.create(number=5, letter='A', school=self.school, teacher=self.teacher_user)
        self.child_user.classroom = self.classroom
        self.child_user.save()

        # Создаем категории, уровни, предметы, этапы и олимпиады
        self.category = Category.objects.create(name='Test Category')
        self.level = LevelOlympiad.objects.create(name='Test Level')
        self.subject = Subject.objects.create(name='Test Subject')
        self.school_stage = Stage.objects.create(name='Школьный')
        self.olympiad = Olympiad.objects.create(
            name='Test Olympiad',
            stage=self.school_stage,
            category=self.category,
            level=self.level,
            subject=self.subject,
            class_olympiad=5
        )

        # Создаем клиент для тестирования
        self.client = Client()

    def test_register_page_access(self):
        """Тест доступа к странице регистрации на олимпиаду"""
        self.client.login(username=self.child_user.username, password='password')
        response = self.client.get(reverse('register:register-olympiad'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register-olympiad/register-olympiad.html')

    def test_add_register(self):
        """Тест добавления заявки на олимпиаду"""
        self.client.login(username=self.child_user.username, password='password')
        response = self.client.get(reverse('register:register_add', args=[self.olympiad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Register.objects.filter(child=self.child_user, olympiad=self.olympiad).exists())

    def test_delete_register(self):
        """Тест удаления заявки на олимпиаду"""
        self.client.login(username=self.child_user.username, password='password')
        register = Register.objects.create(child=self.child_user, olympiad=self.olympiad, school=self.school)
        response = self.client.get(reverse('register:register_remove', args=[register.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Register.objects.filter(id=register.id).exists())

    def test_register_send(self):
        """Тест отправки заявки на олимпиаду"""
        self.client.login(username=self.child_user.username, password='password')
        register = Register.objects.create(child=self.child_user, olympiad=self.olympiad, school=self.school)
        response = self.client.get(reverse('register:register_send'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RegisterSend.objects.filter(child_send=self.child_user, olympiad_send=self.olympiad).exists())

    def test_basket_student_app(self):
        """Тест страницы корзины заявок ученика"""
        self.client.login(username=self.child_user.username, password='password')
        response = self.client.get(reverse('register:basket-student-applications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket-student-applications/basket-student-applications.html')

    def test_child_register_list(self):
        """Тест списка заявок учеников для учителя"""
        self.client.login(username=self.teacher_user.username, password='password')
        response = self.client.get(reverse('register:student-applications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student-applications/student-applications.html')

    def test_register_delete_teacher(self):
        """Тест удаления заявки учителем"""
        self.client.login(username=self.teacher_user.username, password='password')
        register_send = RegisterSend.objects.create(
            teacher_send=self.teacher_user, child_send=self.child_user, olympiad_send=self.olympiad, school=self.school)
        response = self.client.post(
            reverse('register:register_delete_teacher', args=[self.olympiad.id, self.child_user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RegisterSend.objects.filter(id=register_send.id).exists())

    def test_add_recommendation(self):
        """Тест добавления рекомендации учителем"""
        self.client.login(username=self.teacher_user.username, password='password')
        response = self.client.post(reverse('register:add_recommendation'), {
            'child': [self.child_user.id],
            'olympiad': self.olympiad.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recommendation.objects.filter(child=self.child_user, olympiad=self.olympiad).exists())

    def test_register_list_classroom(self):
        """Тест списка заявок от учителей для администратора"""
        self.client.login(username=self.admin_user.username, password='password')
        response = self.client.get(reverse('register:applications-from-classroom-teachers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applications-from-classroom-teachers/register_classroom_admin.html')

    def test_add_register_admin(self):
        """Тест добавления заявки администратором"""
        self.client.login(username=self.admin_user.username, password='password')
        classroom = Classroom.objects.create(number=5, letter='A', school=self.school, teacher=self.teacher_user)
        response = self.client.post(reverse('register:add_register'), {
            'classroom': classroom.id,
            'student': self.child_user.id,
            'olympiad': self.olympiad.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            RegisterAdmin.objects.filter(child_admin=self.child_user, olympiad_admin=self.olympiad).exists())

    def test_teacher_recommendations_view(self):
        """Тест страницы рекомендаций учителя"""
        self.client.login(username=self.teacher_user.username, password='password')
        response = self.client.get(reverse('register:teacher_recommendations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommendations/recommendations.html')

    def test_get_olympiads_for_student(self):
        """Тест получения списка олимпиад для ученика"""
        self.client.login(username=self.teacher_user.username, password='password')
        response = self.client.get(reverse('register:get_olympiads_for_student'), {'student_id': self.child_user.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['olympiads'][0]['name'], 'Test Olympiad')

    def test_get_students_for_classroom(self):
        """Тест получения списка учеников для класса"""
        self.client.login(username=self.admin_user.username, password='password')
        response = self.client.get(reverse('register:get_students_for_classroom'), {'classroom_id': self.classroom.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['students'][0]['name'], self.child_user.get_full_name())
