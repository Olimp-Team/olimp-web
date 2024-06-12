from django.urls import path
from .views import *


app_name = 'docs'
urlpatterns = [
    path('export/excel/', ExcelAll.as_view(), name='export_excel'),
    path('export/excel/classroom/<int:Classroom_id>/', ExcelClassroom.as_view(), name='excel_classroom'),
    path('import/users', import_users, name='import_users'),
    path('success/', lambda request: render(request, 'docs/succes_import.html'), name='succes_import'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('export/dashboard/', ExportExcelView.as_view(), name='export_excel_result'),
    # path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('download/zip/', create_zip_archive, name='download_applications_zip'),
    path('download/teacher/zip/', create_zip_archive_for_teacher, name='download_teacher_applications_zip'),
    path('import_olympiads/', import_olympiads, name='import_olympiads'),
]
