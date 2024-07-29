from django.urls import path
from .views import HomePageView, OlympiadListView, OlympiadCreateView, OlympiadUpdateView, OlympiadDeleteView, AuditLogView

app_name = 'main'

urlpatterns = [
    # Главная страница
    path('', HomePageView.as_view(), name='home'),

    # Страницы для администратора
    path('olympiad/list/', OlympiadListView.as_view(), name='list_olympiad'),
    path('olympiad/new/', OlympiadCreateView.as_view(), name='olympiad_create'),
    path('olympiad/edit/<int:pk>/', OlympiadUpdateView.as_view(), name='olympiad_update'),
    path('olympiad/delete/<int:pk>/', OlympiadDeleteView.as_view(), name='olympiad_delete'),
    path('audit/', AuditLogView.as_view(), name='audit_log'),
]
