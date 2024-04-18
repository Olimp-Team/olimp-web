from django.shortcuts import render

from main.models import Subject
from users.models import User
from .serializers import ChildrenApiSerializers
from rest_framework.views import APIView
from rest_framework.response import Response


class ChildrenApiReact(APIView):
    def get(self, request, format=None):
        output = [
            {
                "username": output.username,
                "first_name": output.first_name,
                "last_name": output.last_name,
                "email": output.email,
                "is_staff": output.is_staff,
                "is_active": output.is_active,
                "date_joined": output.date_joined,
                "surname": output.surname,
                "birth_date": output.birth_date,
                "gender": output.gender,
                "is_child": output.is_child,
                "password": output.password,
                # "classroom": output.classroom,

            } for output in User.objects.all()
        ]
        return Response(output)

    def post(self, request, format=None):
        serializer = ChildrenApiSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
