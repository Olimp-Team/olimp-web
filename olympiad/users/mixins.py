from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


# Миксин для доступа только администратора
class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            # Перенаправляем на страницу доступа запрещен
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


# Миксин для доступа только ученика
class ChildRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_child:
            # Перенаправляем на страницу доступа запрещен
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


# Миксин для доступа только учителя
class TeacherRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            # Перенаправляем на страницу доступа запрещен
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)