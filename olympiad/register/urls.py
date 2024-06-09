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
    path('delete-register/<int:Olympiad_id>/<int:student_id>/', RegisterDeleteTeacher.as_view(),
         name='delete_register'),

    path('add-recommendation/', AddRecommendation.as_view(), name='add_recommendation'),
    path('process-recommendation/', ProcessRecommendation.as_view(), name='process_recommendation'),


    path('applications/classroom/teachers/', RegisterListClassroom.as_view(),
         name='applications-from-classroom-teachers'),
]
