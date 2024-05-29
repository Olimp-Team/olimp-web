from django.urls import path
from .views import *
from .views_child import *
from .views_teacher import *
from .views_admin import *

app_name = 'main'

urlpatterns = [

    # Страницы учеников
    path('home/', HomePage.as_view(), name='home'),
    path('register/olympiad/', RegisterPage.as_view(), name='register-olympiad'),
    path('register/olympiad/add/<int:Olympiad_id>/', RegisterAdd.as_view(), name='register_add'),
    path('register/olympiad/delete/<int:Register_id>/', RegisterDelete.as_view(), name='register_remove'),
    path('basket/student/', BasketStudentApp.as_view(), name='basket-student-applications'),
    path('register/send/', RegisterSend.as_view(), name='register_send'),

    # Страницы учителей
    path('student/applications/', StudentApp.as_view(), name='student-applications'),
    path('register/send/teacher/', RegisterSendTeacher.as_view(), name='register_send_teacher'),
    path('olympiad/teach/delete/<int:Register_id>/', RegisterRemoveTeacher.as_view(), name='register_remove_teacher'),
    path('classroom/teacher/', TeacherClassroomGuide.as_view(), name='TeacherClassroomGuide'),
    path('classroom/teacher/list/<int:Classroom_id>/', ChildrenListTeacher.as_view(), name='ChildrenListTeacher'),

    # Страницы администратора
    path('applications/classroom/teachers/', RegisterListClassroom.as_view(),
         name='applications-from-classroom-teachers'),
    path('classroom/list/', ListClassroom.as_view(), name='list_classroom'),
    path('student/applications/admin/<int:Classroom_id>/', StudentAdminApp.as_view(),
         name='student-applications-admin'),
    path('child/remove/<int:User_id>', ChildRemoveAdmin.as_view(), name='child_remove_admin'),
    path('result/list/olympiad/', ResultListOlympiad.as_view(), name='result-list_olympiad'),
    path('olympiad/list/', ListOlympiad.as_view(), name='list_olympiad'),
    path('result/<int:olymp_id>', Result.as_view(), name='result'),
    path('delete/olympiad/<int:Olympiad_id>', OlympiadDelete.as_view(), name='olympiad_remove'),
    path('create/admin/', CreateAdmin.as_view(), name='CreateAdmin'),
    path('create/child/', CreateChild.as_view(), name='CreateChild'),
    path('create/teacher/', CreateTeacher.as_view(), name='CreateTeacher'),
    # path('create/olympiad',), разработка
    # path('create/classroom',), разработка
    # path('import/', upload_excel, name='import_excel'),

]
