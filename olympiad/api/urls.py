from rest_framework import routers
from .views import *
from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('users-list/', UserApi.as_view(), name='users-list'),
    path('teacher-list/', UserteacherApi.as_view(), name='teacher-list'),
    path('children-list/', UserchildApi.as_view(), name='children-list'),
    path('admin-list/', UseradminApi.as_view(), name='admin-list'),
    path('classroom-list/', ClassroomApi.as_view(), name='classroom-list'),
    path('subject-list/', SubjectApi.as_view(), name='subject-list'),
    path('category-list/', СategoryApi.as_view(), name='category-list'),
    path('level_olympiad-list/', Level_olympiadApi.as_view(), name='level_olympiad-list'),
    path('stage-list/', StageApi.as_view(), name='stage-list'),
    path('post-list/', PostApi.as_view(), name='post-list'),
    path('olympiad-list/', OlympiadApi.as_view(), name='olympiad-list'),
    path('register-list/', RegisterApi.as_view(), name='register-list'),
    path('register_send-list/', Register_sendApi.as_view(), name='register_send-list'),
    path('register_admin-list/', Register_adminApi.as_view(), name='register_admin-list'),
    path('result-list/', ResultApi.as_view(), name='result-list'),

]
