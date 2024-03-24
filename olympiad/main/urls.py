from django.urls import path
from .views import *
from .views import ExportToExcelView

app_name = 'main'

urlpatterns = [
    # Страницы учеников
    path('home/', home, name='home'),
    path('register-olympiad/', register_olympiad, name='register-olympiad'),
    path('register-olympiad/add/<int:Olympiad_id>/', register_add, name='register_add'),
    path('register-olympiad/delete/<int:Register_id>/', register_remove, name='register_remove'),
    path('basket-student-applications/', basket_student_applications, name='basket-student-applications'),
    path('register-send/', register_send, name='register_send'),

    # Страницы учителей
    path('student-applications/', student_applications, name='student-applications'),
    path('register_send_teacher/', register_send_teacher, name='register_send_teacher'),
    path('olympiad_teach/delete/<int:Register_id>/', register_remove_teacher, name='register_remove_teacher'),

    # Страницы администратора
    path('applications-from-classroom-teachers/', register_list_classroom, name='applications-from-classroom-teachers'),
    path('list-classroom/', list_classroom, name='list_classroom'),
    path('student-applications-admin/<int:Classroom_id>/', student_applications_admin, name='student-applications-admin'),
    path('child-remove-admin/<int:User_id>', child_remove_admin, name='child_remove_admin'),
    path('export-excel/', ExportToExcelView.as_view(), name='export_excel'),
    path('export-excel-classroom/<int:Classroom_id>/', excel_classroom, name='excel_classroom'),
    # path('import/', upload_excel, name='import_excel'),

    # # API TEST

]
