from django.urls import path
from .views import *

app_name = 'register'

urlpatterns = [
    path('olympiad/', RegisterPage.as_view(), name='register-olympiad'),
    path('olympiad/add/<int:Olympiad_id>/', RegisterAdd.as_view(), name='register_add'),
    path('olympiad/delete/<int:Register_id>/', RegisterDelete.as_view(), name='register_remove'),
    path('basket/student/', BasketStudentApp.as_view(), name='basket-student-applications'),
    path('send/', RegisterSend.as_view(), name='register_send'),
    path('send/teacher/', RegisterSendTeacher.as_view(), name='register_send_teacher'),
    path('child/list/', ChildRegisterList.as_view(), name='student-applications'),
    path('delete/<int:Olympiad_id>/<int:student_id>/', RegisterDeleteTeacher.as_view(),
         name='register_delete_teacher'),
    path('add-recommendation/', AddRecommendation.as_view(), name='add_recommendation'),
    path('process-recommendation/', ProcessRecommendation.as_view(), name='process_recommendation'),
    path('register/accept_recommendation/<int:recommendation_id>/', accept_recommendation, name='accept_recommendation'),
    path('register/reject_recommendation/<int:recommendation_id>/', reject_recommendation, name='reject_recommendation'),
    path('applications/classroom/teachers/', RegisterListClassroom.as_view(),
         name='applications-from-classroom-teachers'),
    path('get-olympiads-for-student/', GetOlympiadsForStudent.as_view(), name='get_olympiads_for_student'),
]
