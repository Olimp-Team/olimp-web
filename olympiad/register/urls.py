from django.urls import path
from .views import *

app_name = 'register'

urlpatterns = [
    # Регистрация на олимпиаду
    path('olympiad/', RegisterPage.as_view(), name='register-olympiad'),
    path('olympiad/add/<int:Olympiad_id>/', RegisterAdd.as_view(), name='register_add'),
    path('olympiad/delete/<int:Register_id>/', RegisterDelete.as_view(), name='register_remove'),

    # Корзина заявок студентов
    path('basket/student/', BasketStudentApp.as_view(), name='basket-student-applications'),

    # Отправка заявки
    path('send/', RegisterSend.as_view(), name='register_send'),
    path('send/teacher/', RegisterSendTeacher.as_view(), name='register_send_teacher'),

    # Список заявок студентов
    path('child/list/', ChildRegisterList.as_view(), name='student-applications'),

    # Удаление заявки учителем
    path('delete/<int:Olympiad_id>/<int:student_id>/', RegisterDeleteTeacher.as_view(), name='register_delete_teacher'),

    # Рекомендации от учителя
    path('teacher/recommendations/', TeacherRecommendationsView.as_view(), name='teacher_recommendations'),
    path('add-recommendation/', AddRecommendation.as_view(), name='add_recommendation'),

    # Обработка рекомендаций
    path('register/accept_recommendation/<int:recommendation_id>/', accept_recommendation,
         name='accept_recommendation'),
    path('register/reject_recommendation/<int:recommendation_id>/', reject_recommendation,
         name='reject_recommendation'),

    # Заявки от учителей по классам
    path('applications/classroom/teachers/', RegisterListClassroom.as_view(),
         name='applications-from-classroom-teachers'),

    # Получение олимпиад для студента
    path('get-olympiads-for-student/', GetOlympiadsForStudent.as_view(), name='get_olympiads_for_student'),

    # Добавление заявки
    path('add_register/', AddRegister.as_view(), name='add_register'),

    # Получение студентов для класса
    path('get-students-for-classroom/', GetStudentsForClassroomView.as_view(), name='get_students_for_classroom'),

    # Получение олимпиад для студента
    path('get-olympiads-for-student/', GetOlympiadsForStudentView.as_view(), name='get_olympiads_for_student'),
]
