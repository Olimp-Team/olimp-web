from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

from .forms import UserLoginForm, NewAdminForm, NewChildForm, NewTeacherForm
from .views import AuthLogin, CreateAdmin, CreateChild, CreateTeacher, TeacherListView, AdminListView, EditTeacherView, \
    EditAdminView, DeleteUserView

User = get_user_model()


class UserViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных, которые будут использоваться в тестах."""
        cls.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True,
                                                  school='TestSchool')
        cls.teacher_user = User.objects.create_user(username='teacher', password='teacherpass', is_teacher=True,
                                                    school='TestSchool')
        cls.child_user = User.objects.create_user(username='child', password='childpass', is_child=True,
                                                  school='TestSchool')
        cls.client = Client()

        # Вход под пользователем с правами администратора
        cls.client.login(username='admin', password='adminpass')

    def test_login_view(self):
        """Проверка доступности страницы входа."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/auth 2.html')

    def test_login_valid(self):
        """Проверка успешного входа с корректными данными."""
        response = self.client.post(reverse('users:login'),
                                    data={'username': 'admin', 'password': 'adminpass', 'school': 'TestSchool'})
        self.assertRedirects(response, reverse('main:home'))

    def test_create_admin_view(self):
        """Проверка доступности страницы создания администратора."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('users:CreateAdmin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_admin/add_admin.html')

    def test_create_admin_valid(self):
        """Проверка успешного создания администратора с корректными данными."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('users:CreateAdmin'), data={
            'username': 'newadmin',
            'password1': 'newadminpass',
            'password2': 'newadminpass',
            'school': 'TestSchool'
        })
        self.assertRedirects(response, reverse('users:admin_list'))
        new_admin = User.objects.get(username='newadmin')
        self.assertTrue(new_admin.is_admin)

    def test_create_child_view(self):
        """Проверка доступности страницы создания ученика."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('users:CreateChild'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_students/add_students.html')

    def test_create_child_valid(self):
        """Проверка успешного создания ученика с корректными данными."""
        # Создаем класс для ученика
        classroom = Classroom.objects.create(name='Class 1', school='TestSchool')
        response = self.client.post(reverse('users:CreateChild'), data={
            'username': 'newchild',
            'password1': 'newchildpass',
            'password2': 'newchildpass',
            'school': 'TestSchool',
            'classroom': classroom.id
        })
        self.assertRedirects(response, reverse('classroom:list_classroom'))
        new_child = User.objects.get(username='newchild')
        self.assertTrue(new_child.is_child)

    def test_create_teacher_view(self):
        """Проверка доступности страницы создания учителя."""
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('users:CreateTeacher'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_teacher/add_teacher.html')

    def test_create_teacher_valid(self):
        """Проверка успешного создания учителя с корректными данными."""
        response = self.client.post(reverse('users:CreateTeacher'), data={
            'username': 'newteacher',
            'password1': 'newteacherpass',
            'password2': 'newteacherpass',
            'school': 'TestSchool'
        })
        self.assertRedirects(response, reverse('users:teacher_list'))
        new_teacher = User.objects.get(username='newteacher')
        self.assertTrue(new_teacher.is_teacher)

    def test_teacher_list_view(self):
        """Проверка доступности страницы со списком учителей."""
        response = self.client.get(reverse('users:teacher_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_list.html')
        self.assertContains(response, self.teacher_user.username)

    def test_admin_list_view(self):
        """Проверка доступности страницы со списком администраторов."""
        response = self.client.get(reverse('users:admin_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_list.html')
        self.assertContains(response, self.admin_user.username)

    def test_edit_teacher_view(self):
        """Проверка доступности страницы редактирования учителя."""
        response = self.client.get(reverse('users:edit_teacher', args=[self.teacher_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_teacher.html')

    def test_edit_teacher_valid(self):
        """Проверка успешного редактирования данных учителя."""
        response = self.client.post(reverse('users:edit_teacher', args=[self.teacher_user.id]), data={
            'username': 'updatedteacher',
            'password1': 'teacherpass',
            'password2': 'teacherpass'
        })
        self.assertRedirects(response, reverse('users:teacher_list'))
        self.teacher_user.refresh_from_db()
        self.assertEqual(self.teacher_user.username, 'updatedteacher')

    def test_edit_admin_view(self):
        """Проверка доступности страницы редактирования администратора."""
        response = self.client.get(reverse('users:edit_admin', args=[self.admin_user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_admin.html')

    def test_edit_admin_valid(self):
        """Проверка успешного редактирования данных администратора."""
        response = self.client.post(reverse('users:edit_admin', args=[self.admin_user.id]), data={
            'username': 'updatedadmin',
            'password1': 'adminpass',
            'password2': 'adminpass'
        })
        self.assertRedirects(response, reverse('users:admin_list'))
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.username, 'updatedadmin')

    def test_delete_user_view(self):
        """Проверка успешного удаления пользователя."""
        response = self.client.post(reverse('users:delete_user', args=[self.teacher_user.id]))
        self.assertRedirects(response, reverse('users:teacher_list'))
        self.assertFalse(User.objects.filter(id=self.teacher_user.id).exists())
