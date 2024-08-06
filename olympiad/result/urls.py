from django.urls import path
from .views import *

app_name = 'result'

urlpatterns = [
    path('add/', OlympiadResultCreateView.as_view(), name='add_result'),
    path('add/classroom/', OlympiadResultClassCreateView.as_view(), name='add_result_class'),
    path('get_students/', GetStudentsView.as_view(), name='get_students'),  # Новый URL для AJAX-представления
    path('list/', ResultListView.as_view(), name='results_list'),
    path('import-results/', ImportResultsView.as_view(), name='import_results'),
    path('export-results/', ExportResultsView.as_view(), name='export_results'),
    path('student/results/', StudentResultListView.as_view(), name='student_results'),
    path('get_olympiads/', GetOlympiadsView.as_view(), name='get_olympiads'),

    ### test
    path('create/', ResultCreateView.as_view(), name='result_create'),
    path('ajax/load-students/', load_students, name='ajax_load_students'),
    path('ajax/load-olympiads/', load_olympiads, name='ajax_load_olympiads'),
]

# Описание каждого пути:
# path('add/', OlympiadResultCreateView.as_view(), name='add_result')
# Представление для добавления результата олимпиады.

# path('add/classroom/', OlympiadResultClassCreateView.as_view(), name='add_result_class')
# Представление для добавления результатов олимпиады для всего класса.

# path('get_students/', GetStudentsView.as_view(), name='get_students')
# AJAX-представление для получения списка учеников.

# path('list/', ResultListView.as_view(), name='results_list')
# Представление для отображения списка результатов.

# path('import-results/', ImportResultsView.as_view(), name='import_results')
# Представление для импорта результатов.

# path('export-results/', ExportResultsView.as_view(), name='export_results')
# Представление для экспорта результатов.

# path('student/results/', StudentResultListView.as_view(), name='student_results')
# Представление для отображения результатов конкретного ученика.

# path('get_olympiads/', GetOlympiadsView.as_view(), name='get_olympiads')
# AJAX-представление для получения списка олимпиад.
