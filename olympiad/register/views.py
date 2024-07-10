from django.http import HttpResponseForbidden, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from main.models import *
from register.models import *
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


########################################################################################################################
# Страницы учеников


# class RegisterPage(ChildRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_child:
#             school_stage = Stage.objects.get(name='Школьный')
#             olympiads = Olympiad.objects.filter(class_olympiad=request.user.classroom.number, stage=school_stage)
#             registered_olympiads = Register.objects.filter(child=request.user).values_list('Olympiad_id', flat=True)
#             context = {
#                 'olympiads': olympiads,
#                 'olympiads_last': olympiads.last(),
#                 'registered_olympiads': registered_olympiads
#             }
#             return render(request, 'register-olympiad/register-olympiad.html', context)
#         else:
#             return HttpResponseForbidden()


class RegisterPage(ChildRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_child:
            school_stage = Stage.objects.get(name='Школьный')
            olympiads = Olympiad.objects.filter(class_olympiad=request.user.classroom.number, stage=school_stage)

            # Получаем список олимпиад, на которые ученик зарегистрировался, исключая удаленные заявки
            registered_olympiads = Register_send.objects.filter(
                child_send=request.user,
                is_deleted=False
            ).values_list('Olympiad_send_id', flat=True)

            context = {
                'olympiads': olympiads,
                'olympiads_last': olympiads.last(),
                'registered_olympiads': registered_olympiads
            }
            return render(request, 'register-olympiad/register-olympiad.html', context)
        else:
            return HttpResponseForbidden()


class RegisterAdd(ChildRequiredMixin, View):
    def get(self, request, Olympiad_id):
        if request.user.is_child:
            olympiad = Olympiad.objects.get(id=Olympiad_id)
            if olympiad.stage.name != 'Школьный':
                return HttpResponseForbidden('Регистрация возможна только на школьный этап.')

            # Проверяем, есть ли удаленная заявка на эту олимпиаду
            register = Register.objects.filter(child=request.user, Olympiad=olympiad).first()
            if register and register.status_send:
                register_send = Register_send.objects.filter(child_send=request.user, Olympiad_send=olympiad).first()
                if register_send and register_send.is_deleted:
                    # Обновляем статус удаленной заявки
                    register_send.is_deleted = False
                    register_send.status_send = False
                    register_send.save()
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])

            # Создаем или обновляем заявку в Register
            register, created = Register.objects.update_or_create(
                child=request.user,
                Olympiad=olympiad,
                defaults={'teacher': request.user.classroom.teacher}
            )

            if not created:
                register.save()

            # Создаем или обновляем заявку в Register_send
            Register_send.objects.update_or_create(
                teacher_send=request.user.classroom.teacher,
                child_send=request.user,
                Olympiad_send=olympiad,
                defaults={'is_deleted': False, 'status_send': False, 'status_teacher': False, 'status_admin': False}
            )

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class RegisterDelete(ChildRequiredMixin, View):
    def get(self, request, Register_id):
        if request.user.is_child:
            register_basket = Register.objects.get(id=Register_id)
            register_basket.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


import logging

logger = logging.getLogger(__name__)


class RegisterSend(ChildRequiredMixin, View):
    def get(self, request):
        if request.user.is_child:
            register_entries = Register.objects.filter(child=request.user, status_send=False)
            for entry in register_entries:
                if entry.teacher and entry.child and entry.Olympiad:
                    existing_register_send = Register_send.objects.filter(
                        teacher_send=entry.teacher,
                        child_send=entry.child,
                        Olympiad_send=entry.Olympiad
                    ).first()

                    if existing_register_send:
                        existing_register_send.is_deleted = False
                        existing_register_send.status_send = False
                        existing_register_send.save()
                    else:
                        Register_send.objects.create(
                            teacher_send=entry.teacher,
                            child_send=entry.child,
                            Olympiad_send=entry.Olympiad,
                            status_send=False
                        )

            register_entries.update(status_send=True)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        pass


class BasketStudentApp(ChildRequiredMixin, View):
    def get(self, request):
        if request.user.is_child:
            context = {
                'register': Register.objects.filter(child=request.user, status_send=False),
                'recommendations': Recommendation.objects.filter(child=request.user, status=False),
                'register_sends': Register_send.objects.filter(child_send=request.user),
                'deleted_registers': Register_send.objects.filter(child_send=request.user, is_deleted=True),
            }
            return render(request, 'basket-student-applications/basket-student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if request.user.is_child:
            action = request.POST.get('action')
            olympiad_id = request.POST.get('olympiad_id')
            if not action or not olympiad_id:
                return HttpResponseForbidden("Missing data in form.")

            olympiad = get_object_or_404(Olympiad, id=olympiad_id)

            if action == 're-register':
                # Создаем или обновляем заявку в Register
                register, created = Register.objects.update_or_create(
                    child=request.user,
                    Olympiad=olympiad,
                    defaults={'teacher': request.user.classroom.teacher}
                )

                if not created:
                    register.save()

                # Также создаем или обновляем заявку в Register_send
                Register_send.objects.update_or_create(
                    teacher_send=request.user.classroom.teacher,
                    child_send=request.user,
                    Olympiad_send=olympiad,
                    defaults={'is_deleted': False, 'status_send': False, 'status_teacher': False, 'status_admin': False}
                )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return HttpResponseForbidden()


########################################################################################################################
# Страницы учителей
class ChildRegisterList(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            # Получаем класс, которым руководит текущий пользователь
            classroom_guide = request.user.classroom_guide

            # Получаем все заявки учеников, которые связаны с классом текущего учителя
            reg = Register_send.objects.filter(
                teacher_send__classroom_guide=classroom_guide,
                status_send=False,
                is_deleted=False,
            )

            # Создаем словарь, где ключом будет ученик, а значением - список олимпиад
            student_olympiads = {}
            for register in reg:
                if register.child_send not in student_olympiads:
                    student_olympiads[register.child_send] = []
                student_olympiads[register.child_send].append(register.Olympiad_send)

            # Получаем отправленные заявки для текущего учителя
            sent_applications = Register_send.objects.filter(
                teacher_send__classroom_guide=classroom_guide,
                status_send=True,
                is_deleted=False,
            )

            # Создаем словарь, где ключом будет ученик, а значением - список олимпиад
            sent_applications_dict = {}
            for application in sent_applications:
                if application.child_send not in sent_applications_dict:
                    sent_applications_dict[application.child_send] = []
                sent_applications_dict[application.child_send].append(application.Olympiad_send)

            # Получаем рекомендации для текущего учителя
            recommendations = Recommendation.objects.filter(recommended_to=request.user, status=False)
            recommended_students = {}
            for rec in recommendations:
                if rec.child not in recommended_students:
                    recommended_students[rec.child] = []
                recommended_students[rec.child].append({
                    'olympiad': rec.Olympiad,
                    'recommended_by': rec.recommended_by,
                    'id': rec.id,
                })

            context = {
                'student_olympiads': student_olympiads,
                'recommended_students': recommended_students,
                'sent_applications': sent_applications_dict,
            }
            return render(request, 'student-applications/student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        return HttpResponseForbidden()


def accept_recommendation(request, recommendation_id):
    if not request.user.is_teacher:
        return HttpResponseForbidden()

    recommendation = get_object_or_404(Recommendation, id=recommendation_id)

    Register_send.objects.create(
        teacher_send=request.user,
        child_send=recommendation.child,
        Olympiad_send=recommendation.Olympiad,
        status_send=False,
        is_deleted=False,
    )
    recommendation.status = True
    recommendation.save()

    return redirect('register:student-applications')


def reject_recommendation(request, recommendation_id):
    if not request.user.is_teacher:
        return HttpResponseForbidden()

    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    recommendation.status = True
    recommendation.save()

    return redirect('register:student-applications')


class RegisterDeleteTeacher(TeacherRequiredMixin, View):
    def post(self, request, Olympiad_id, student_id):
        if request.user.is_teacher:
            try:
                register = Register_send.objects.get(Olympiad_send_id=Olympiad_id, child_send_id=student_id,
                                                     is_deleted=False)
                register.is_deleted = True
                register.save()
                # Запись действия в аудит
                AuditLog.objects.create(
                    user=request.user,
                    action='Удаление заявки',
                    object_name=f'Заявка ученика {register.child_send.get_full_name()} на олимпиаду {register.Olympiad_send.name}'
                )
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except Register_send.DoesNotExist:
                return HttpResponseForbidden("Заявка не найдена.")
        else:
            return HttpResponseForbidden()


class RegisterSendTeacher(TeacherRequiredMixin, View):
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
                    defaults={'status_teacher': True, 'status_admin': False, 'is_deleted': register.is_deleted}
                )
            # Обновляем статус заявок в Register_send
            registers.update(status_send=True)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class AddRecommendation(TeacherRequiredMixin, View):
    def get(self, request):
        if request.user.is_teacher:
            school_stage = Stage.objects.get(name='Школьный')
            context = {
                'students': User.objects.filter(is_child=True),
                'olympiads': Olympiad.objects.filter(stage=school_stage),
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
            # Запись действия в аудит
            AuditLog.objects.create(
                user=request.user,
                action='Создание рекомендации',
                object_name=f'Рекомендация ученику {child.get_full_name()} на олимпиаду {olympiad.name}'
            )
            return HttpResponseRedirect(reverse_lazy('main:home'))
        else:
            return HttpResponseForbidden()


class GetOlympiadsForStudent(View):
    def get(self, request):
        school_stage = Stage.objects.get(name='Школьный')
        student_id = request.GET.get('student_id')
        student = User.objects.get(id=student_id)
        olympiads = Olympiad.objects.filter(class_olympiad=student.classroom.number, stage=school_stage)
        olympiads_data = [
            {
                'id': olympiad.id,
                'name': olympiad.name,
                'stage': olympiad.stage.name,
                'class': olympiad.class_olympiad
            }
            for olympiad in olympiads
        ]
        return JsonResponse({'olympiads': olympiads_data})


class ProcessRecommendation(TeacherRequiredMixin, View):
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

class RegisterListClassroom(AdminRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            # Получаем все заявки и группируем их по учебным классам
            registers = Register_admin.objects.filter(is_deleted=False)
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
