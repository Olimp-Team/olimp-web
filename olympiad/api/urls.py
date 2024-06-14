from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'registers', RegisterViewSet)
router.register(r'results', ResultViewSet)
router.register(r'olympiads', OlympiadViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'registers_admin', RegisterAdminViewSet)
router.register(r'registers_send', RegisterSendViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'levels', LevelOlympiadViewSet)
router.register(r'stages', StageViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
