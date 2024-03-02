from django.urls import path
from .views import *
from .views import ExportToExcelView, UsersAPIView

app_name = 'main'

urlpatterns = [
    # Страницы учеников
    path('home/', home, name='home'),
    path('register-olympiad/', register, name='register-olympiad'),
    path('olympiad/add/<int:Olympiad_id>/', register_add, name='register_add'),
    path('olympiad/delete/<int:Register_id>/', register_remove, name='register_remove'),
    path('basket-student-applications/', register_spis, name='basket-student-applications'),
    # Страницы учителей
    path('student-applications/', student_applications, name='student-applications'),
    # Страницы администратора
    path('applications-from-classroom-teachers/', register_list_classroom, name='applications-from-classroom-teachers'),
    path('export-excel/', ExportToExcelView.as_view(), name='export_excel'),
    # path('import/', upload_excel, name='import_excel'),
    # API TEST
    path('api/users-list/', UsersAPIView.as_view(), name='users-list')
]
