from django.urls import path
from .views import *

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

]
