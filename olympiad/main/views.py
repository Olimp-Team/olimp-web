from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from result.models import *
from .forms import *
from .filters import *
from raiting_system.models import *


def page_not_found(request, exception):
    return HttpResponseNotFound('К сожалению, страница не найдена.')


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'homepage/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получение последних 10 результатов для текущего пользователя
        recent_results = Result.objects.filter(info_children=self.request.user,
                                               school=self.request.user.school).order_by('-date_added')[:10]
        context['recent_results'] = recent_results

        # Получение рейтинга пользователя
        user_rating = Rating.objects.filter(user=self.request.user).first()
        context['user_rating'] = user_rating

        # Расчеты для лиг
        points = user_rating.points if user_rating else 0
        if points <= 150:
            league = 'Бронзовая лига'
            points_to_next = 151 - points
        elif points <= 500:
            league = 'Серебряная лига'
            points_to_next = 501 - points
        elif points <= 1000:
            league = 'Золотая лига'
            points_to_next = 1001 - points
        elif points <= 2000:
            league = 'Платиновая лига'
            points_to_next = 2001 - points
        elif points <= 3500:
            league = 'Рубиновая лига'
            points_to_next = 3501 - points
        else:
            league = 'Алмазная лига'
            points_to_next = 0

        context['league'] = league
        context['points_to_next'] = points_to_next

        # Получение медалей пользователя
        user_medals = Medal.objects.filter(user=self.request.user)
        context['user_medals'] = user_medals

        # Получение именных медалей пользователя
        user_personal_medals = PersonalMedal.objects.filter(user=self.request.user)
        context['user_personal_medals'] = user_personal_medals

        return context


class AuditLogView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'audit_log/audit_log.html'
    context_object_name = 'audit_logs'
    ordering = ['-timestamp']

    def get_queryset(self):
        # Отображаем только для администраторов
        if self.request.user.is_admin:
            return super().get_queryset()
        else:
            return AuditLog.objects.none()


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
