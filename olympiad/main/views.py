from django.http import HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from result.models import Result
from raiting_system.models import Rating, Medal, PersonalMedal
from .forms import OlympiadForm
from .filters import OlympiadFilter
from .models import AuditLog, Olympiad


def page_not_found(request, exception):
    """
    Обработчик ошибки 404.
    """
    return HttpResponseNotFound('К сожалению, страница не найдена.')


class HomePageView(LoginRequiredMixin, TemplateView):
    """
    Представление для главной страницы.
    """
    template_name = 'homepage/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение последних 10 результатов для текущего пользователя
        recent_results = Result.objects.filter(info_children=self.request.user, school=self.request.user.school).order_by('-date_added')[:10]
        context['recent_results'] = recent_results

        # Получение рейтинга пользователя
        user_rating = Rating.objects.filter(user=self.request.user).first()
        context['user_rating'] = user_rating

        # Расчеты для лиг
        points = user_rating.points if user_rating else 0
        league, points_to_next = self.calculate_league(points)
        context['league'] = league
        context['points_to_next'] = points_to_next

        # Получение медалей пользователя
        user_medals = Medal.objects.filter(user=self.request.user)
        context['user_medals'] = user_medals

        # Получение именных медалей пользователя
        user_personal_medals = PersonalMedal.objects.filter(user=self.request.user)
        context['user_personal_medals'] = user_personal_medals

        # Получение олимпиад
        olympiads = Olympiad.objects.order_by('date')
        context['olympiads'] = olympiads

        return context

    def calculate_league(self, points):
        """
        Вспомогательный метод для расчета лиги и очков до следующей лиги.
        """
        if points <= 150:
            return 'Бронзовая лига', 151 - points
        elif points <= 500:
            return 'Серебряная лига', 501 - points
        elif points <= 1000:
            return 'Золотая лига', 1001 - points
        elif points <= 2000:
            return 'Платиновая лига', 2001 - points
        elif points <= 3500:
            return 'Рубиновая лига', 3501 - points
        else:
            return 'Алмазная лига', 0


class AuditLogView(LoginRequiredMixin, ListView):
    """
    Представление для отображения журнала аудита.
    """
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
    """
    Представление для отображения списка олимпиад.
    """
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
    """
    Представление для создания новой олимпиады.
    """
    model = Olympiad
    form_class = OlympiadForm
    template_name = 'list_olympiad/olympiad_form.html'
    success_url = reverse_lazy('main:list_olympiad')


class OlympiadUpdateView(UpdateView):
    """
    Представление для обновления существующей олимпиады.
    """
    model = Olympiad
    form_class = OlympiadForm
    template_name = 'list_olympiad/olympiad_form.html'
    success_url = reverse_lazy('main:list_olympiad')


class OlympiadDeleteView(DeleteView):
    """
    Представление для удаления олимпиады.
    """
    model = Olympiad
    template_name = 'list_olympiad/olympiad_confirm_delete.html'
    success_url = reverse_lazy('main:list_olympiad')
