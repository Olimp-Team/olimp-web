from django.urls import path
from .views import *


app_name = 'docs'
urlpatterns = [
    path('export/excel/', ExcelAll.as_view(), name='export_excel'),
    path('export/excel/classroom/<int:Classroom_id>/', ExcelClassroom.as_view(), name='excel_classroom'),
    path('export/dashboard/', ExportExcelView.as_view(), name='export_excel_result'),
    path('import/users', import_users.as_view(), name='import_users'),
    path('import_olympiads/', import_olympiads.as_view(), name='import_olympiads'),
    path('download/zip/', create_zip_archive.as_view(), name='download_applications_zip'),
    path('download/teacher/zip/', create_zip_archive_for_teacher.as_view(), name='download_teacher_applications_zip'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('success/', lambda request: render(request, 'docs/succes_import.html'), name='succes_import'),
    path('success/olympiad', lambda request: render(request, 'docs/succes_import_olympiad.html'), name='succes_import_olympiad'),


]
