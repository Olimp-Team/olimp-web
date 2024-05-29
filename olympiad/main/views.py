from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import *
from users.forms import NewChildForm
from .decorators import *
from .models import Register, Register_admin
from .forms import ResultCreateFrom
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


def page_not_found(request, exception):
    return HttpResponseNotFound('Sorry, you are not allowed to see this page.')


class HomePage(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'homepage/homepage.html', )
