from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    AuthLogin,
    logout,
    PasswordChange,
    CreateAdmin,
    CreateChild,
    CreateTeacher,
    TeacherListView,
    AdminListView,
    EditTeacherView,
    EditAdminView,
    DeleteUserView
)
from friends.views import ProfileView
from .forms import CustomPasswordResetForm

app_name = 'users'

urlpatterns = [
    # URL для страницы входа
    path('login/', AuthLogin.as_view(), name='login'),

    # URL для профиля пользователя по его ID
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),

    # URL для выхода из системы
    path('logout/', logout, name='logout'),

    # URL для изменения пароля
    path('password_change/', PasswordChange.as_view(), name='password_change'),

    # URL для создания администратора
    path('create/admin/', CreateAdmin.as_view(), name='CreateAdmin'),

    # URL для создания ученика
    path('create/child/', CreateChild.as_view(), name='CreateChild'),

    # URL для создания учителя
    path('create/teacher/', CreateTeacher.as_view(), name='CreateTeacher'),

    # URL для списка учителей
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),

    # URL для списка администраторов
    path('admins/', AdminListView.as_view(), name='admin_list'),

    # URL для редактирования информации об учителе
    path('teachers/edit/<int:pk>/', EditTeacherView.as_view(), name='edit_teacher'),

    # URL для редактирования информации об администраторе
    path('admins/edit/<int:pk>/', EditAdminView.as_view(), name='edit_admin'),

    # URL для удаления пользователя
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),

    # URL для сброса пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        success_url=reverse_lazy('users:password_reset_done'),
        form_class=CustomPasswordResetForm,
        email_template_name='auth/password_reset_email.html',
    ), name='password_reset'),

    # URL для подтверждения сброса пароля
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html',
         ),
         name='password_reset_done'),

    # URL для подтверждения сброса пароля по ссылке
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('users:password_reset_complete')
         ),
         name='password_reset_confirm'),

    # URL для завершения сброса пароля
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # URL для обновления Telegram ID (закомментировано, если потребуется в будущем)
    # path('update_telegram_id/', update_telegram_id, name='update_telegram_id'),
]
