from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Модель пользователей в панели администратора"""
    list_display = [
        'id',  # Отображение ID пользователя
        'username',  # Отображение имени пользователя
        'first_name',  # Отображение имени
        'last_name',  # Отображение фамилии
        'surname',  # Отображение отчества
        'email',  # Отображение электронной почты
        'is_staff',  # Отображение флага сотрудника
        'is_active',  # Отображение флага активности
    ]
    list_editable = [
        'username',  # Возможность редактирования имени пользователя
        'first_name',  # Возможность редактирования имени
        'last_name',  # Возможность редактирования фамилии
        'surname',  # Возможность редактирования отчества
        'email',  # Возможность редактирования электронной почты
        'is_staff',  # Возможность редактирования флага сотрудника
        'is_active',  # Возможность редактирования флага активности
    ]
    ordering = ['id']  # Сортировка пользователей по ID
    search_fields = ['last_name', 'first_name']  # Поля для поиска пользователей по фамилии и имени
