from django.contrib import admin
from register.models import Register, RegisterSend, RegisterAdmin, Recommendation


@admin.register(Register)
class RegisterAdminModel(admin.ModelAdmin):
    """Регистрация модели Register в админке"""
    list_display = ('id', 'school', 'teacher', 'child', 'olympiad', 'status_send', 'is_deleted')
    search_fields = ('child__last_name', 'child__first_name', 'olympiad__name')
    list_filter = ('status_send', 'is_deleted', 'school')


@admin.register(RegisterSend)
class RegisterSendAdminModel(admin.ModelAdmin):
    """Регистрация модели RegisterSend в админке"""
    list_display = (
    'id', 'school', 'teacher_send', 'child_send', 'olympiad_send', 'status_teacher', 'status_admin', 'status_send',
    'is_deleted')
    search_fields = ('child_send__last_name', 'child_send__first_name', 'olympiad_send__name')
    list_filter = ('status_teacher', 'status_admin', 'status_send', 'is_deleted', 'school')


@admin.register(RegisterAdmin)
class RegisterAdminAdminModel(admin.ModelAdmin):
    """Регистрация модели RegisterAdmin в админке"""
    list_display = (
    'id', 'school', 'teacher_admin', 'child_admin', 'olympiad_admin', 'status_admin', 'status_teacher', 'is_deleted')
    search_fields = ('child_admin__last_name', 'child_admin__first_name', 'olympiad_admin__name')
    list_filter = ('status_admin', 'status_teacher', 'is_deleted', 'school')


@admin.register(Recommendation)
class RecommendationAdminModel(admin.ModelAdmin):
    """Регистрация модели Recommendation в админке"""
    list_display = ('id', 'school', 'recommended_by', 'recommended_to', 'child', 'olympiad', 'status')
    search_fields = ('recommended_by__last_name', 'recommended_by__first_name', 'recommended_to__last_name',
                     'recommended_to__first_name', 'child__last_name', 'child__first_name', 'olympiad__name')
    list_filter = ('status', 'school')
