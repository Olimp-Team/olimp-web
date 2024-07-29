from django.contrib import admin
from result.models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Настройки отображения модели Result в панели администратора"""

    # Определяем поля, которые будут отображаться в списке
    list_display = ('id', 'info_children', 'info_olympiad', 'points', 'status_result')

    # Поля, которые можно редактировать прямо из списка
    list_editable = ['info_children', 'info_olympiad', 'points', 'status_result']

    # Поля, по которым можно выполнять поиск
    search_fields = ['status_result', 'points', 'info_olympiad', 'info_children']

    # Добавляем сортировку по умолчанию (например, по id)
    ordering = ['id']

    # Добавляем возможность фильтрации по статусу результата
    list_filter = ['status_result']
