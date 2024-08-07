from django.contrib import admin
from main.models import *




@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Модель учебных предметов в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(Category)
class СategoryAdmin(admin.ModelAdmin):
    """Модель категорий олимпиад в панеле администратора"""
    list_display = ('id', 'name',)
    list_editable = ['name']
    search_fields = ['name']


@admin.register(LevelOlympiad)
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


@admin.register(Olympiad)
class OlympiadAdmin(admin.ModelAdmin):
    """Модель олимпиад в панеле администратора"""
    list_display = (
        'id', 'name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad')
    list_editable = ['name', 'description', 'category', 'level', 'stage', 'subject', 'class_olympiad']
    search_fields = ['name', 'class_olympiad', 'category', 'level', 'stage', 'subject']
