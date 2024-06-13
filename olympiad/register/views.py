from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from main.models import *
from register.models import *
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


########################################################################################################################
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
            if olympiad.stage.name != 'Школьный':
                return HttpResponseForbidden('Регистрация возможна только на школьный этап.')

            register, created = Register.objects.get_or_create(
                child=request.user,
                Olympiad=olympiad,
                defaults={'teacher': request.user.classroom.teacher}
            )

            if not created:
                register.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request):
        return HttpResponseForbidden()


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


class BasketStudentApp(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_child:
            context = {
                'register': Register.objects.filter(child=request.user, status_send=False),
                'recommendations': Recommendation.objects.filter(child=request.user, status=False),
            }
            return render(request, 'basket-student-applications/basket-student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        recommendation_id = request.POST.get('recommendation_id')
        if not action or not recommendation_id:
            return HttpResponseForbidden("Missing data in form.")

        recommendation = get_object_or_404(Recommendation, id=recommendation_id)

        if action == 'accept':
            Register.objects.create(
                child=request.user,
                teacher=request.user.classroom.teacher,
                Olympiad=recommendation.Olympiad,
                status_send=False
            )
            recommendation.status = True
            recommendation.save()
        elif action == 'decline':
            recommendation.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


########################################################################################################################
# Страницы учителей
class ChildRegisterList(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            # Получаем все заявки учеников, которые связаны с классом текущего учителя
            reg = Register_send.objects.filter(
                teacher_send__classroom_guide=request.user.classroom_guide,
                status_send=False,
                is_deleted=False,
            )

            # Создаем словарь, где ключом будет ученик, а значением - список олимпиад
            student_olympiads = {}
            for register in reg:
                if register.child_send not in student_olympiads:
                    student_olympiads[register.child_send] = []
                student_olympiads[register.child_send].append(register.Olympiad_send)

            # Получаем рекомендации для текущего учителя
            recommendations = Recommendation.objects.filter(recommended_to=request.user, status=False)
            recommended_students = {}
            for rec in recommendations:
                if rec.child not in recommended_students:
                    recommended_students[rec.child] = []
                recommended_students[rec.child].append({
                    'olympiad': rec.Olympiad,
                    'recommended_by': rec.recommended_by
                })

            context = {
                'student_olympiads': student_olympiads,
                'recommended_students': recommended_students,
            }
            return render(request, 'student-applications/student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if request.user.is_teacher:
            return HttpResponseForbidden()


class RegisterDeleteTeacher(View, LoginRequiredMixin):
    def post(self, request, Olympiad_id, student_id):
        if request.user.is_teacher:
            try:
                register = Register_send.objects.get(Olympiad_send_id=Olympiad_id, child_send_id=student_id,
                                                     is_deleted=False)
                register.is_deleted = True
                register.save()
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except Register_send.DoesNotExist:
                return HttpResponseForbidden("Заявка не найдена.")
        else:
            return HttpResponseForbidden()


class RegisterSendTeacher(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            # Получаем заявки от текущего учителя, которые ещё не были обработаны
            registers = Register_send.objects.filter(
                teacher_send=request.user,
                status_send=False
            )
            for register in registers:
                # Обновляем существующую запись или создаем новую, если не существует
                Register_admin.objects.update_or_create(
                    teacher_admin=register.teacher_send,
                    child_admin=register.child_send,
                    Olympiad_admin=register.Olympiad_send,
                    defaults={'status_teacher': True, 'status_admin': False}
                )
            # Обновляем статус заявок в Register
            registers.update(status_send=True)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class AddRecommendation(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_teacher:
            context = {
                'students': User.objects.filter(is_child=True, classroom__teacher=request.user),
                'olympiads': Olympiad.objects.all(),
                'teachers': User.objects.filter(is_teacher=True)
            }
            return render(request, 'add-recommendation/add-recommendation.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if request.user.is_teacher:
            recommended_to = User.objects.get(id=request.POST['recommended_to'])
            child = User.objects.get(id=request.POST['child'])
            olympiad = Olympiad.objects.get(id=request.POST['olympiad'])

            Recommendation.objects.create(
                recommended_by=request.user,
                recommended_to=recommended_to,
                child=child,
                Olympiad=olympiad
            )
            return HttpResponseRedirect(reverse_lazy('main:home'))
        else:
            return HttpResponseForbidden()


class ProcessRecommendation(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return HttpResponseForbidden("Permission denied.")

        student_id = request.POST.get('student_id')
        recommended_by_id = request.POST.get('recommended_by_id')
        olympiad_id = request.POST.get('olympiad_id')
        action = request.POST.get('action')

        print(student_id, recommended_by_id, olympiad_id, action)  # Для отладки

        if not student_id:
            return HttpResponseForbidden("Missing student_id")
        if not recommended_by_id:
            return HttpResponseForbidden("Missing recommended_by_id")
        if not olympiad_id:
            return HttpResponseForbidden("Missing olympiad_id")
        if not action:
            return HttpResponseForbidden("Missing action")

        student = get_object_or_404(User, pk=student_id)
        recommended_by = get_object_or_404(User, pk=recommended_by_id)
        olympiad = get_object_or_404(Olympiad, pk=olympiad_id)

        if action == 'accept':
            Register_send.objects.create(
                teacher_send=request.user,
                child_send=student,
                Olympiad_send=olympiad,
                status_send=False
            )
            recommendation = get_object_or_404(
                Recommendation,
                recommended_by=recommended_by,
                recommended_to=request.user,
                child=student,
                Olympiad=olympiad
            )
            recommendation.status = True
            recommendation.save()
        elif action == 'decline':
            Recommendation.objects.filter(
                recommended_by=recommended_by,
                recommended_to=request.user,
                child=student,
                Olympiad=olympiad
            ).delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


########################################################################################################################
# Страницы администратора

class RegisterListClassroom(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_admin:
            # Получаем все заявки и группируем их по учебным классам
            registers = Register_admin.objects.all()
            grouped_registers = {}
            for register in registers:
                classroom = register.child_admin.classroom  # Предполагаем, что у модели child_admin есть поле classroom
                if classroom not in grouped_registers:
                    grouped_registers[classroom] = []
                grouped_registers[classroom].append(register)

            context = {
                'grouped_registers': grouped_registers
            }
            return render(request, 'applications-from-classroom-teachers/register_classroom_admin.html',
                          context)
        else:
            return HttpResponseForbidden()
