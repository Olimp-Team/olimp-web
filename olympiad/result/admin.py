from django.contrib import admin
from result.models import *


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Модель результатов олимпиад в панеле администратора"""
    list_display = ('id', 'info_children', 'info_olympiad', 'points', 'status_result')
    list_editable = ['info_children', 'info_olympiad', 'points', 'status_result']
    search_fields = ['status_result', 'points', 'info_olympiad', 'info_children']
