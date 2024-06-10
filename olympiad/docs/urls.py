from django.urls import path
from .views import *


app_name = 'docs'
urlpatterns = [
    path('export/excel/', ExcelAll.as_view(), name='export_excel'),
    path('export/excel/classroom/<int:Classroom_id>/', ExcelClassroom.as_view(), name='excel_classroom'),
    path('import/users', import_users, name='import_users'),
    path('success/', lambda request: render(request, 'docs/success.html'), name='success'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('export/dashboard/', ExportExcelView.as_view(), name='export_excel')
]
