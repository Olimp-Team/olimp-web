from django.http import HttpResponseForbidden


def is_teacher(view_func):
    """Декоратор прав доступа для учителей"""

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_teacher:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return wrapper_func


def is_child(view_func):
    """Декоратор прав доступа для администраторов"""

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_child:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return wrapper_func


def is_admin(view_func):
    """Декоратор прав доступа для администраторов"""

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return wrapper_func
