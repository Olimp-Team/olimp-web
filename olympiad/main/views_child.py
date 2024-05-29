from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from .models import *
from .decorators import *
from .models import Register
from django.views.generic import *
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


# Страницы учеников

class RegisterPage(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_child:
            context = {
                'olympiads': Olympiad.objects.filter(class_olympiad=request.user.classroom.number),
                'olympiads_last': Olympiad.objects.filter(class_olympiad=request.user.classroom.number).last()
            }
            return render(request, 'register-olympiad/register-olympiad.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if request.user.is_child:
            pass
        else:
            return HttpResponseForbidden()


class RegisterAdd(View, LoginRequiredMixin):
    def get(self, request, Olympiad_id):
        if request.user.is_child:
            olympiad = Olympiad.objects.get(id=Olympiad_id)
            registers = Register.objects.filter(child=request.user, Olympiad=olympiad)
            if not registers.exists():
                Register.objects.create(child=request.user, Olympiad=olympiad, teacher=request.user.classroom.teacher)
            else:
                basket = registers.first()
                basket.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if request.user.is_child:
            pass
        else:
            return HttpResponseForbidden()


class RegisterAdd(View, LoginRequiredMixin):
    def get(self, request, Olympiad_id):
        if request.user.is_child:
            olympiad = Olympiad.objects.get(id=Olympiad_id)
            registers = Register.objects.filter(child=request.user, Olympiad=olympiad)
            if not registers.exists():
                Register.objects.create(child=request.user, Olympiad=olympiad, teacher=request.user.classroom.teacher)
            else:
                basket = registers.first()
                basket.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class RegisterDelete(View, LoginRequiredMixin):
    def get(self, request, Register_id):
        if request.user.is_child:
            register_basket = Register.objects.get(id=Register_id)
            register_basket.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class BasketStudentApp(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_child:
            context = {
                'register': Register.objects.filter(child=request.user, status_send=False)
            }
            return render(request, 'basket-student-applications/basket-student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class RegisterSend(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_child:
            objs = [
                Register_send(
                    teacher_send=i.teacher,
                    child_send=i.child,
                    Olympiad_send=i.Olympiad,
                )
                for i in Register.objects.filter(child=request.user, status_send=False)
            ]

            Register_send.objects.bulk_create(objs)
            Register.objects.filter(child=request.user).update(status_send=True)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass
