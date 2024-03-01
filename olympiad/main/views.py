from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from main.models import *
from rest_framework.views import APIView
from users.models import Users
from django.http import HttpResponse
from django.views.generic import View
from django.utils.translation import gettext as _
from excel_response import ExcelResponse
from rest_framework import generics
from .decorators import *
import pandas as pd
from .serializers import UsersSerializer
from .forms import ExcelUploadForm


# Страницы учеников
@login_required
def home(request):
    return render(request, 'homepage/homepage.html')


@login_required
@is_child
def register(request):
    context = {
        'olympiads': Olympiad.objects.all()
    }
    return render(request, 'register-olympiad/register-olympiad.html', context)


@login_required
@is_child
def register_add(request, Olympiad_id):
    olympiad = Olympiad.objects.get(id=Olympiad_id)
    registers = Register.objects.filter(user=request.user, Olympiad=olympiad)

    if not registers.exists():
        Register.objects.create(user=request.user, Olympiad=olympiad)
    else:
        basket = registers.first()
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@is_child
def register_remove(request, Register_id):
    register_basket = Register.objects.get(id=Register_id)
    register_basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
@is_child
def register_spis(request):
    context = {
        'register-olympiad-olympiad': Register.objects.all()
    }
    return render(request, 'basket-student-applications/basket-student-applications.html', context)


# Страницы учителей
@login_required
@is_teacher
def register_list(request):
    reg = Register.objects.all()
    context = {
        'register-olympiad-olympiad': reg
    }
    return render(request, 'student-applications/student-applications.html', context)

# Страницы администратора
@login_required
@is_admin
def register_list_classroom(request):
    return render(request, 'applications-from-classroom-teachers/applications-from-classroom-teachers.html')


class ExportToExcelView(View):
    def get(self, request):
        queryset = Register.objects.all()  # Получаем данные из нашей модели
        data = [
            [_("№"), _("Фамилия"), _("Имя"), _("Отчество"),
             _("Пол"), _("Дата рождения"), _("Олимпиада"), ],
            # Заголовки столбцов
        ]
        for obj in queryset:
            data.append([
                obj.user.id,
                obj.user.last_name,
                obj.user.first_name,
                obj.user.surname,
                obj.user.gender,
                obj.user.birth_date,
                obj.Olympiad.name,
            ])

        return ExcelResponse(data, 'Регистрация')  # - имя файла Excel


class UsersAPIView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
