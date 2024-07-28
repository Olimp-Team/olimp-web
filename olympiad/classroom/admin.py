from django.contrib import admin
from classroom.models import *
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """Модель учебных классов в панеле администратора"""
    list_display = ['id', 'number', 'letter', 'teacher']
    list_editable = ['number', 'letter']
    search_fields = ['letter', 'number']
