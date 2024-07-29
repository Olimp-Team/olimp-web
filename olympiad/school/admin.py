from django.contrib import admin
from school.models import School


@admin.register(School)
class SchoolAdminModel(admin.ModelAdmin):
    """
    Административная панель для модели School.
    """
    list_display = ('name', 'address', 'contact_email', 'contact_phone')  # Поля, отображаемые в списке объектов
    search_fields = ('name', 'address', 'contact_email', 'contact_phone')  # Поля, доступные для поиска



