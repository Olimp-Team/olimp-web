from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


# Миксин для проверки доступа только для администратора
class AdminRequiredMixin(AccessMixin):
    """
    Миксин, который позволяет доступ только пользователям с правами администратора.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            raise PermissionDenied  # Выбрасывает ошибку, если пользователь не администратор
        return super().dispatch(request, *args, **kwargs)


# Миксин для проверки доступа только для ученика
class ChildRequiredMixin(AccessMixin):
    """
    Миксин, который позволяет доступ только пользователям с правами ученика.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_child:
            raise PermissionDenied  # Выбрасывает ошибку, если пользователь не ученик
        return super().dispatch(request, *args, **kwargs)


# Миксин для проверки доступа только для учителя
class TeacherRequiredMixin(AccessMixin):
    """
    Миксин, который позволяет доступ только пользователям с правами учителя.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            raise PermissionDenied  # Выбрасывает ошибку, если пользователь не учитель
        return super().dispatch(request, *args, **kwargs)
