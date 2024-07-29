from django.test import TestCase, Client
from django.urls import reverse
from .models import School
from users.models import User

class SchoolRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('school:register_school')

    def test_register_school_view_get(self):
        """Тест отображения страницы регистрации школы"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_school.html')

    def test_register_school_success(self):
        """Тест успешной регистрации школы и создания администратора"""
        data = {
            'name': 'Test School',
            'address': '123 Test St',
            'contact_email': 'test@school.com',
            'contact_phone': '1234567890',
            'admin_username': 'adminuser',
            'admin_password': 'adminpass123',
            'admin_email': 'admin@school.com',
            'admin_first_name': 'Admin',
            'admin_last_name': 'User',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления после успешной регистрации
        self.assertTrue(School.objects.filter(name='Test School').exists())  # Проверка создания записи школы
        self.assertTrue(User.objects.filter(username='adminuser').exists())  # Проверка создания администратора

    def test_register_school_invalid_data(self):
        """Тест регистрации школы с некорректными данными"""
        data = {
            'name': '',
            'address': '123 Test St',
            'contact_email': 'invalid-email',
            'contact_phone': '1234567890',
            'admin_username': 'adminuser',
            'admin_password': 'adminpass123',
            'admin_email': 'admin@school.com',
            'admin_first_name': 'Admin',
            'admin_last_name': 'User',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Проверка, что страница перезагружается с ошибками
        self.assertFalse(School.objects.filter(name='').exists())  # Проверка, что школа не создана
        self.assertFalse(User.objects.filter(username='adminuser').exists())  # Проверка, что администратор не создан

    def test_register_school_duplicate_school(self):
        """Тест регистрации школы с уже существующим именем"""
        School.objects.create(
            name='Existing School',
            address='123 Existing St',
            contact_email='existing@school.com',
            contact_phone='0987654321'
        )
        data = {
            'name': 'Existing School',
            'address': '123 Test St',
            'contact_email': 'test@school.com',
            'contact_phone': '1234567890',
            'admin_username': 'adminuser',
            'admin_password': 'adminpass123',
            'admin_email': 'admin@school.com',
            'admin_first_name': 'Admin',
            'admin_last_name': 'User',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Проверка, что страница перезагружается с ошибками
        self.assertEqual(School.objects.filter(name='Existing School').count(), 1)  # Проверка, что школа не дублируется
        self.assertFalse(User.objects.filter(username='adminuser').exists())  # Проверка, что администратор не создан

    def test_register_school_missing_fields(self):
        """Тест регистрации школы с отсутствующими полями"""
        data = {
            'name': 'Test School',
            'address': '123 Test St',
            'contact_email': '',
            'contact_phone': '1234567890',
            'admin_username': '',
            'admin_password': 'adminpass123',
            'admin_email': 'admin@school.com',
            'admin_first_name': 'Admin',
            'admin_last_name': 'User',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Проверка, что страница перезагружается с ошибками
        self.assertFalse(School.objects.filter(name='Test School').exists())  # Проверка, что школа не создана
        self.assertFalse(User.objects.filter(email='admin@school.com').exists())  # Проверка, что администратор не создан
