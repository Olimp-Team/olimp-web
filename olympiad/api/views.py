from django.shortcuts import render
from rest_framework import viewsets, generics
from users.models import User
from main.models import *

from .serializers import *


class UserApi(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserteacherApi(generics.ListAPIView):
    queryset = User.objects.filter(is_teacher=True)
    serializer_class = UserSerializer


class UserchildApi(generics.ListAPIView):
    queryset = User.objects.filter(is_child=True)
    serializer_class = UserSerializer


class UseradminApi(generics.ListAPIView):
    queryset = User.objects.filter(is_admin=True)
    serializer_class = UserSerializer


class ClassroomApi(generics.ListAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class SubjectApi(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class СategoryApi(generics.ListAPIView):
    queryset = Сategory.objects.all()
    serializer_class = СategorySerializer


class Level_olympiadApi(generics.ListAPIView):
    queryset = Level_olympiad.objects.all()
    serializer_class = Level_olympiadSerializer


class StageApi(generics.ListAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer


class PostApi(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class OlympiadApi(generics.ListAPIView):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer


class RegisterApi(generics.ListAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer


class Register_sendApi(generics.ListAPIView):
    queryset = Register_send.objects.all()
    serializer_class = Register_sendSerializer


class Register_adminApi(generics.ListAPIView):
    queryset = Register_admin.objects.all()
    serializer_class = Register_adminSerializer


class ResultApi(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
