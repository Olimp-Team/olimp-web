from rest_framework import viewsets, generics
from .serializers import *
from users.models import User
from .serializers import AuthUser
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib import auth


class AuthApi(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = AuthUser(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if AuthUser.data not in request.data:
            return Response(['Метод POST не доступен'], status=400)

        if 'password' not in request.data:
            return Response(['Метод POST не доступен'], status=400)

