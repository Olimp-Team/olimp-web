from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('export/excel/', ExcelAll.as_view(), name='export_excel'),
    path('export/excel/classroom/<int:Classroom_id>/', ExcelClassroom.as_view(), name='excel_classroom'),
]
