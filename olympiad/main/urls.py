from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    # Страницы учеников
    path('home/', HomePage.as_view(), name='home'),
    path('register-olympiad/', RegisterPage.as_view(), name='register-olympiad'),
    path('register-olympiad/add/<int:Olympiad_id>/', RegisterAdd.as_view(), name='register_add'),
    path('register-olympiad/delete/<int:Register_id>/', RegisterDelete.as_view(), name='register_remove'),
    path('basket-student-applications/', BasketStudentApp.as_view(), name='basket-student-applications'),
    path('register-send/', RegisterSend.as_view(), name='register_send'),

    # Страницы учителей
    path('student-applications/', StudentApp.as_view(), name='student-applications'),
    path('register_send_teacher/', RegisterSendTeacher.as_view(), name='register_send_teacher'),
    path('olympiad_teach/delete/<int:Register_id>/', RegisterRemoveTeacher.as_view(), name='register_remove_teacher'),

    # Страницы администратора
    path('applications-from-classroom-teachers/', RegisterListClassroom.as_view(),
         name='applications-from-classroom-teachers'),
    path('list-classroom/', ListClassroom.as_view(), name='list_classroom'),
    path('student-applications-admin/<int:Classroom_id>/', StudentAdminApp.as_view(),
         name='student-applications-admin'),
    path('child-remove-admin/<int:User_id>', ChildRemoveAdmin.as_view(), name='child_remove_admin'),
    path('export-excel/', ExcelAll.as_view(), name='export_excel'),
    path('export-excel-classroom/<int:Classroom_id>/', ExcelClassroom.as_view(), name='excel_classroom'),
    path('result-list-olympiad/', ResultListOlympiad.as_view(), name='result-list_olympiad'),
    path('list-olympiad/', ListOlympiad.as_view(), name='list_olympiad'),
    path('result/<int:olymp_id>', Result.as_view(), name='result'),
    path('delete/olympiad/<int:Olympiad_id>', OlympiadDelete.as_view(), name='olympiad_remove'),
    path('create/admin/', CreateAdmin.as_view(), name='CreateAdmin'),
    path('create/child/', CreateChild.as_view(), name='CreateChild'),
    path('create/teacher/', CreateTeacher.as_view(), name='CreateTeacher'),
    # path('create/olympiad',), разработка
    # path('create/classroom',), разработка
    # path('import/', upload_excel, name='import_excel'),

]
