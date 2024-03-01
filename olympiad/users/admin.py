from django.contrib import admin

from users.models import Users
from main.admin import ClassroomAdmin, PostAdmin


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    # Модель пользователей в панеле администратора
    list_display = ['id',
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                    'surname',
                    'email',
                    'is_staff',
                    'is_active', ]
    list_editable = [
        'username',
        'password',
        'first_name',
        'last_name',
        'surname',
        'email',
        'is_staff',
        'is_active', ]
    ordering = ['id']
    search_fields = ['last_name', 'first_name', ]
