from django.contrib import admin


class OlympiadAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'location', 'category', 'level', 'stage', 'subject', 'class_olympiad')

# Регистрация моделей из django-scheduler в админке
