from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from django.views.generic import *
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from result.models import *


def page_not_found(request, exception):
    return HttpResponseNotFound('К сожалению, страница не найдена.')


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'homepage/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_results = Result.objects.filter(info_children=self.request.user).order_by('-date_added')[
                         :10]  # Получение последних 10 результатов для текущего пользователя
        context['recent_results'] = recent_results
        return context


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
