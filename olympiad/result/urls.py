from django.urls import path
from .views import *

app_name = 'result'

urlpatterns = [
    path('add/', OlympiadResultCreateView.as_view(), name='add_result'),
    path('add/classroom/', OlympiadResultClassCreateView.as_view(), name='add_result_class'),
    path('get_students/', get_students.as_view(), name='get_students'),  # Новый URL для AJAX-представления
    path('list/', ResultListView.as_view(), name='results_list'),
    path('import-results/', ImportResultsView.as_view(), name='import_results'),
    path('export-results/', ExportResultsView.as_view(), name='export_results'),

]
