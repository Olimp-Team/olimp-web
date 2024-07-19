from django.urls import path
from .views import *

app_name = 'classroom'

urlpatterns = [
    path('teacher/list/<int:Classroom_id>/', ChildrenListTeacher.as_view(), name='ChildrenListTeacher'),
    path('teacher/', TeacherClassroomGuide.as_view(), name='TeacherClassroomGuide'),
    path('classroom/list/', ClassroomListView.as_view(), name='list_classroom'),
    path('child-expel/<int:User_id>/', ChildExpelAdmin.as_view(), name='child_expel_admin'),
    path('child-reinstate/<int:User_id>/', ChildReinstateAdmin.as_view(), name='child_reinstate_admin'),
    path('student/applications/admin/<int:Classroom_id>/', ChildClassroomListAdmin.as_view(),
         name='student-applications-admin'),
    path('new/', ClassroomCreateView.as_view(), name='classroom_create'),
    path('edit/<int:pk>/', ClassroomUpdateView.as_view(), name='classroom_update'),
    path('delete/<int:pk>/', ClassroomDeleteView.as_view(), name='classroom_delete'),
    path('promote_all/', PromoteAllClassroomsView.as_view(), name='promote_all_classrooms'),
]
