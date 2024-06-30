from django.urls import path, reverse_lazy
from .views import *
from django.contrib.auth import views as auth_views
from .forms import *

app_name = 'users'

urlpatterns = [
    path('login/', AuthLogin.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('create/admin/', CreateAdmin.as_view(), name='CreateAdmin'),
    path('create/child/', CreateChild.as_view(), name='CreateChild'),
    path('create/teacher/', CreateTeacher.as_view(), name='CreateTeacher'),
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('admins/', AdminListView.as_view(), name='admin_list'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset.html',
        success_url=reverse_lazy('users:password_reset_done'),
        form_class=CustomPasswordResetForm,
        email_template_name='auth/password_reset_email.html', ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html', ),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),

]
