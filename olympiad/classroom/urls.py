from django.urls import path
from .views import *

app_name = 'classroom'

urlpatterns = [
    path('teacher/list/<int:Classroom_id>/', ChildrenListTeacher.as_view(), name='ChildrenListTeacher'),
    path('teacher/', TeacherClassroomGuide.as_view(), name='TeacherClassroomGuide'),
    path('classroom/list/', ListClassroom.as_view(), name='list_classroom'),
    path('child/remove/<int:User_id>', ChildRemoveAdmin.as_view(), name='child_remove_admin'),
    path('student/applications/admin/<int:Classroom_id>/', ChildClassroomListAdmin.as_view(),
         name='student-applications-admin'),
    path('new/', ClassroomCreateView.as_view(), name='classroom_create'),
    path('edit/<int:pk>/', ClassroomUpdateView.as_view(), name='classroom_update'),
    path('delete/<int:pk>/', ClassroomDeleteView.as_view(), name='classroom_delete'),
]
