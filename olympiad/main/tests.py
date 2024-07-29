from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from result.models import Result
from raiting_system.models import Rating, Medal, PersonalMedal
from main.models import AuditLog, Olympiad, Category, LevelOlympiad, Stage, Subject
from school.models import School
from django.utils import timezone

User = get_user_model()

class MainViewsTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Создание тестовой школы
        self.school = School.objects.create(name='Test School')

        # Создание тестового пользователя с указанием школы
        self.user = User.objects.create_user(username='testuser', password='password', is_admin=True, school=self.school)
        self.client.login(username='testuser', password='password')

        self.category = Category.objects.create(name='Test Category')
        self.level = LevelOlympiad.objects.create(name='Test Level')
        self.stage = Stage.objects.create(name='Test Stage')
        self.subject = Subject.objects.create(name='Test Subject')
        self.olympiad = Olympiad.objects.create(
            name='Test Olympiad',
            category=self.category,
            level=self.level,
            stage=self.stage,
            subject=self.subject,
            class_olympiad=10,
            date=timezone.now().date(),
            time=timezone.now().time()
        )

    def test_home_page_view(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/homepage.html')
        self.assertIn('recent_results', response.context)
        self.assertIn('user_rating', response.context)
        self.assertIn('league', response.context)
        self.assertIn('points_to_next', response.context)
        self.assertIn('user_medals', response.context)
        self.assertIn('user_personal_medals', response.context)
        self.assertIn('olympiads', response.context)

    def test_olympiad_list_view(self):
        response = self.client.get(reverse('main:list_olympiad'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_olympiad/list_olympiad.html')
        self.assertIn('olympiads', response.context)
        self.assertIn('filterset', response.context)

    def test_olympiad_create_view(self):
        response = self.client.get(reverse('main:olympiad_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_olympiad/olympiad_form.html')

        data = {
            'name': 'New Olympiad',
            'category': self.category.id,
            'level': self.level.id,
            'stage': self.stage.id,
            'subject': self.subject.id,
            'class_olympiad': 9,
            'date': timezone.now().date(),
            'time': timezone.now().time()
        }
        response = self.client.post(reverse('main:olympiad_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Olympiad.objects.filter(name='New Olympiad').exists())

    def test_olympiad_update_view(self):
        response = self.client.get(reverse('main:olympiad_update', args=[self.olympiad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_olympiad/olympiad_form.html')

        data = {
            'name': 'Updated Olympiad',
            'category': self.category.id,
            'level': self.level.id,
            'stage': self.stage.id,
            'subject': self.subject.id,
            'class_olympiad': 11,
            'date': timezone.now().date(),
            'time': timezone.now().time()
        }
        response = self.client.post(reverse('main:olympiad_update', args=[self.olympiad.id]), data)
        self.assertEqual(response.status_code, 302)
        self.olympiad.refresh_from_db()
        self.assertEqual(self.olympiad.name, 'Updated Olympiad')

    def test_olympiad_delete_view(self):
        response = self.client.get(reverse('main:olympiad_delete', args=[self.olympiad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_olympiad/olympiad_confirm_delete.html')

        response = self.client.post(reverse('main:olympiad_delete', args=[self.olympiad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Olympiad.objects.filter(id=self.olympiad.id).exists())

    def test_audit_log_view(self):
        AuditLog.objects.create(user=self.user, action='Test Action', object_name='Test Object', school=self.school)
        response = self.client.get(reverse('main:audit_log'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audit_log/audit_log.html')
        self.assertIn('audit_logs', response.context)
