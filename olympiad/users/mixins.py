from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class ChildRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_child

    def handle_no_permission(self):
        raise PermissionDenied("You do not have child access.")


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher

    def handle_no_permission(self):
        raise PermissionDenied("You do not have teacher access.")


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin

    def handle_no_permission(self):
        raise PermissionDenied("You do not have admin access.")
