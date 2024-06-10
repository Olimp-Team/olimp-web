from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [

    # Страницы учеников
    path('home/', HomePage.as_view(), name='home'),
    # Страницы учителей
    # path('student/applications/', ChildrenListTeacher.as_view(), name='student-applications'),
    path('classroom/teacher/', TeacherClassroomGuide.as_view(), name='TeacherClassroomGuide'),
    path('classroom/teacher/list/<int:Classroom_id>/', ChildrenListTeacher.as_view(), name='ChildrenListTeacher'),
    # Страницы администратора
    path('classroom/list/', ListClassroom.as_view(), name='list_classroom'),
    path('child/remove/<int:User_id>', ChildRemoveAdmin.as_view(), name='child_remove_admin'),
    path('olympiad/list/', ListOlympiad.as_view(), name='list_olympiad'),
    path('delete/olympiad/<int:Olympiad_id>', OlympiadDelete.as_view(), name='olympiad_remove'),
    path('student/applications/admin/<int:Classroom_id>/', ChildClassroomListAdmin.as_view(),
         name='student-applications-admin'),


]
