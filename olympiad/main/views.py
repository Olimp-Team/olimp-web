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
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from result.models import *
from .forms import *
from .filters import *


def page_not_found(request, exception):
    return HttpResponseNotFound('К сожалению, страница не найдена.')


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'homepage/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получение последних 10 результатов для текущего пользователя
        recent_results = Result.objects.filter(info_children=self.request.user).order_by('-date_added')[:10]
        context['recent_results'] = recent_results
        return context


class OlympiadListView(ListView):
    model = Olympiad
    template_name = 'list_olympiad/list_olympiad.html'
    context_object_name = 'olympiads'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = OlympiadFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class OlympiadCreateView(CreateView):
    model = Olympiad
    form_class = OlympiadForm
    template_name = 'list_olympiad/olympiad_form.html'
    success_url = reverse_lazy('main:list_olympiad')


class OlympiadUpdateView(UpdateView):
    model = Olympiad
    form_class = OlympiadForm
    template_name = 'list_olympiad/olympiad_form.html'
    success_url = reverse_lazy('main:list_olympiad')


class OlympiadDeleteView(DeleteView):
    model = Olympiad
    template_name = 'list_olympiad/olympiad_confirm_delete.html'
    success_url = reverse_lazy('main:list_olympiad')
