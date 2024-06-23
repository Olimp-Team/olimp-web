from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponseNotFound
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import *
from users.forms import NewChildForm, NewTeacherForm, NewAdminForm
from .decorators import *
from .forms import ResultCreateFrom
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


def page_not_found(request, exception):
    return HttpResponseNotFound('К сожалению, страница не найдена.')


class HomePage(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'homepage/homepage.html', )


########################################################################################################################
# Страницы учеников

########################################################################################################################
# Страницы учителей

########################################################################################################################
# Страницы администратора

class ListOlympiad(TemplateView, AdminRequiredMixin):
    """ Страница для отображения олимпиад """

    def get(self, request, *args, **kwargs):
        context = {
            'olympiad': Olympiad.objects.filter()
        }
        return render(request, 'list_olympiad/list_olympiad.html', context)


class OlympiadDelete(View, LoginRequiredMixin, AdminRequiredMixin):
    """ Функция для удаления олимпиады"""
    def get(self, request, Olympiad_id):
        olympiad = Olympiad.objects.get(id=Olympiad_id)
        olympiad.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    def post(self, request):
        pass
