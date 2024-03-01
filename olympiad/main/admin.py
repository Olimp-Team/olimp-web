from django.contrib import admin
from main.models import *


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """Модель учебных классов в панеле администратора"""
    list_display = ['id', 'number', 'letter', ]
    list_editable = ['number', 'letter']
    search_fields = ['letter', 'number']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Модель учебных предметов в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Сategory)
class СategoryAdmin(admin.ModelAdmin):
    """Модель категорий олимпиад в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Level_olympiad)
class Level_olympiadAdmin(admin.ModelAdmin):
    """Модель уровней олимпиад в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    """Модель этапов олимпиад в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Модель должностей персонала школы в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Модель учителей в панеле администратора"""
    list_display = ['id',
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                    'surname',
                    'email',
                    'is_staff',
                    'is_active',
                    'classroom_guide', ]
    list_editable = [
        'username',
        'password',
        'first_name',
        'last_name',
        'surname',
        'email',
        'is_staff',
        'is_active',
        'classroom_guide', ]
    ordering = ['id']
    search_fields = ['last_name', 'first_name', ]


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    """Модель учеников в панеле администратора"""
    list_display = ['id',
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                    'surname',
                    'email',
                    'is_staff',
                    'is_active',
                    'classroom', ]
    list_editable = [
        'username',
        'password',
        'first_name',
        'last_name',
        'surname',
        'email',
        'is_staff',
        'is_active',
        'classroom', ]
    ordering = ['id']
    search_fields = ['last_name', 'first_name', ]


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    """Модель администраторов в панеле администратора"""
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
        'is_active',
    ]
    ordering = ['id']
    search_fields = ['last_name', 'first_name', ]


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    """Модель олимпиад в панеле администратора"""
    list_display = (
        'id', 'name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad', 'date_olympiad')
    list_editable = ['name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad', 'date_olympiad']
    search_fields = ['name', 'class_olympiad', 'category', 'level', 'stage', 'subject', 'date_olympiad']


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    """Модель регистрации на олимпиаду в панеле администратора"""
    list_display = ('id', 'user', 'Olympiad')
    list_editable = ['user', 'Olympiad']
    search_fields = ['user', 'Olympiad']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Модель результатов олимпиад в панеле администратора"""
    list_display = ('id', 'info_children', 'info_olympiad', 'points', 'status_result')
    list_editable = ['info_children', 'info_olympiad', 'points', 'status_result']
    search_fields = ['status_result', 'points', 'info_olympiad', 'info_children']



