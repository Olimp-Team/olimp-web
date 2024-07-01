from rest_framework import viewsets
from main.models import *
from register.models import *
from result.models import *
from users.models import *
from .serializers import *
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class OlympiadViewSet(viewsets.ModelViewSet):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class RegisterAdminViewSet(viewsets.ModelViewSet):
    queryset = Register_admin.objects.all()
    serializer_class = RegisterAdminSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class RegisterSendViewSet(viewsets.ModelViewSet):
    queryset = Register_send.objects.all()
    serializer_class = RegisterSendSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class LevelOlympiadViewSet(viewsets.ModelViewSet):
    queryset = Level_olympiad.objects.all()
    serializer_class = LevelOlympiadSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [AllowAny]  # Разрешить доступ без аутентификации
