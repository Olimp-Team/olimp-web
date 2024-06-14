from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied


# Миксин для доступа только администратора
class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# Миксин для доступа только ученика
class ChildRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_child:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# Миксин для доступа только учителя
class TeacherRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
