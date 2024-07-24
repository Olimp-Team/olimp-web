from django.contrib import admin
from school.models import School


@admin.register(School)
class School(admin.ModelAdmin):
    pass
