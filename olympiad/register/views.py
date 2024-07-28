# register/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from main.models import *
from register.models import *
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin
from .form import *
from classroom.models import *


class RegisterPage(ChildRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_child:
            try:
                school_stage = Stage.objects.get(name='Школьный')
            except Stage.DoesNotExist:
                raise Http404("Stage not found")

            olympiads = Olympiad.objects.filter(class_olympiad=request.user.classroom.number, stage=school_stage)
            registered_olympiads = Register.objects.filter(child=request.user).values_list(
                'Olympiad_id', flat=True)
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
            olympiad = get_object_or_404(Olympiad, id=Olympiad_id)
            if olympiad.stage.name != 'Школьный':
                return HttpResponseForbidden('Регистрация возможна только на школьный этап.')

            register, created = Register.objects.update_or_create(
                child=request.user,
                Olympiad=olympiad,
                defaults={'teacher': request.user.classroom.teacher, 'school': request.user.school, 'is_deleted': False,
                          'status_send': False}
            )

            Register.objects.update_or_create(
                teacher=request.user.classroom.teacher,
                child=request.user,
                Olympiad=olympiad,
                defaults={'is_deleted': False, 'status_send': False, 'status_teacher': False, 'status_admin': False,
                          'school': request.user.school}
            )

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class RegisterDelete(ChildRequiredMixin, View):
    def get(self, request, Register_id):
        if request.user.is_child:
            register_basket = get_object_or_404(Register, id=Register_id, school=request.user.school)
            register_basket.delete()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class RegisterSend(ChildRequiredMixin, View):
    def get(self, request):
        if request.user.is_child:
            register_entries = Register.objects.filter(child=request.user, status_send=False,
                                                       school=request.user.school)
            for entry in register_entries:
                Register_send.objects.update_or_create(
                    teacher_send=entry.teacher,
                    child_send=entry.child,
                    Olympiad_send=entry.Olympiad,
                    school=request.user.school,
                    defaults={'status_send': False, 'is_deleted': False, 'status_teacher': False, 'status_admin': False}
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
                'register': Register.objects.filter(child=request.user, status_send=False, school=request.user.school),
                'recommendations': Recommendation.objects.filter(child=request.user, school=request.user.school,
                                                                 status=Recommendation.PENDING),
                'register_sends': Register_send.objects.filter(child_send=request.user, school=request.user.school),
                'deleted_registers': Register_send.objects.filter(child_send=request.user, is_deleted=True,
                                                                  school=request.user.school),
            }
            return render(request, 'basket-student-applications/basket-student-applications.html', context)
        else:
            return HttpResponseForbidden()


class ChildRegisterList(TeacherRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            classroom_guide = request.user.classroom_guide
            reg = Register_send.objects.filter(
                teacher_send__classroom_guide=classroom_guide,
                status_send=False,
                is_deleted=False,
                school=request.user.school
            )

            student_olympiads = {}
            for register in reg:
                if register.child_send not in student_olympiads:
                    student_olympiads[register.child_send] = []
                student_olympiads[register.child_send].append(register.Olympiad_send)

            sent_applications = Register_send.objects.filter(
                teacher_send__classroom_guide=classroom_guide,
                status_send=True,
                is_deleted=False,
                school=request.user.school
            )

            sent_applications_dict = {}
            for application in sent_applications:
                if application.child_send not in sent_applications_dict:
                    sent_applications_dict[application.child_send] = []
                sent_applications_dict[application.child_send].append(application.Olympiad_send)

            context = {
                'student_olympiads': student_olympiads,

                'sent_applications': sent_applications_dict,
            }
            return render(request, 'student-applications/student-applications.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        return HttpResponseForbidden()


def accept_recommendation(request, recommendation_id):
    if not request.user.is_child:
        return HttpResponseForbidden()

    recommendation = get_object_or_404(Recommendation, id=recommendation_id, school=request.user.school)
    Register.objects.update_or_create(
        teacher=recommendation.recommended_by,
        child=recommendation.child,
        Olympiad=recommendation.Olympiad,
        defaults={
            'status_send': False,
            'is_deleted': False,
            'school': request.user.school
        }
    )
    recommendation.status = Recommendation.ACCEPTED
    recommendation.save()

    return redirect('register:basket-student-applications')


def reject_recommendation(request, recommendation_id):
    if not request.user.is_child:
        return HttpResponseForbidden()

    recommendation = get_object_or_404(Recommendation, id=recommendation_id, school=request.user.school)
    recommendation.status = Recommendation.DECLINED
    recommendation.save()

    return redirect('register:basket-student-applications')


class RegisterDeleteTeacher(TeacherRequiredMixin, View):
    def post(self, request, Olympiad_id, student_id):
        if request.user.is_teacher:
            try:
                register_send = Register_send.objects.get(Olympiad_send_id=Olympiad_id, child_send_id=student_id,
                                                          school=request.user.school)
                register_send.delete()

                register = Register.objects.get(Olympiad_id=Olympiad_id, child_id=student_id,
                                                school=request.user.school)
                register.delete()

                AuditLog.objects.create(
                    user=request.user,
                    action='Удаление заявки',
                    school=request.user.school,
                    object_name=f'Заявка ученика {register.child.get_full_name()} на олимпиаду {register.Olympiad.name}'
                )

                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except Register_send.DoesNotExist:
                return HttpResponseForbidden("Заявка не найдена.")
            except Register.DoesNotExist:
                return HttpResponseForbidden("Заявка не найдена.")
        else:
            return HttpResponseForbidden()


class RegisterSendTeacher(TeacherRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            registers = Register_send.objects.filter(
                teacher_send=request.user,
                status_send=False,
                school=request.user.school
            )
            for register in registers:
                Register_admin.objects.update_or_create(
                    teacher_admin=register.teacher_send,
                    child_admin=register.child_send,
                    Olympiad_admin=register.Olympiad_send,
                    defaults={'status_teacher': True, 'status_admin': False, 'is_deleted': register.is_deleted,
                              'school': request.user.school}
                )
            registers.update(status_send=True)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponseForbidden()


class AddRecommendation(TeacherRequiredMixin, View):
    def get(self, request):
        if request.user.is_teacher:
            students = User.objects.filter(is_child=True, school=request.user.school)
            context = {
                'students': students,
                'user': request.user,
            }
            return render(request, 'add-recommendation/add-recommendation.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if request.user.is_teacher:
            recommended_to = request.user
            child_ids = request.POST.getlist('child')
            olympiad_id = request.POST.get('olympiad')

            if not child_ids or not olympiad_id:
                return HttpResponseForbidden("Missing child or olympiad data")

            olympiad = get_object_or_404(Olympiad, id=olympiad_id)

            for child_id in child_ids:
                child = get_object_or_404(User, id=child_id, school=request.user.school)
                Recommendation.objects.create(
                    recommended_by=request.user,
                    recommended_to=recommended_to,
                    child=child,
                    Olympiad=olympiad,
                    school=request.user.school
                )
                AuditLog.objects.create(
                    user=request.user,
                    school=request.user.school,
                    action='Создание рекомендации',
                    object_name=f'Рекомендация ученику {child.get_full_name()} на олимпиаду {olympiad.name}'
                )
            return redirect('register:teacher_recommendations')
        else:
            return HttpResponseForbidden()


import logging

logger = logging.getLogger(__name__)


class GetOlympiadsForStudent(View):
    def get(self, request):
        student_id = request.GET.get('student_id')
        if student_id:
            student = get_object_or_404(User, pk=student_id, is_child=True, school=request.user.school)
            olympiads = Olympiad.objects.filter(class_olympiad=student.classroom.number, stage__name='Школьный')
            olympiads_data = [
                {
                    'id': olympiad.id,
                    'name': olympiad.name,
                    'stage': olympiad.stage.name if olympiad.stage else 'Этап не указан',
                    'class_olympiad': olympiad.class_olympiad if olympiad.class_olympiad else 'Класс не указан'
                }
                for olympiad in olympiads
            ]
            logger.debug('Olympiads data: %s', olympiads_data)
            return JsonResponse({'olympiads': olympiads_data})
        else:
            return JsonResponse({'olympiads': []})


class RegisterListClassroom(AdminRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            registers = Register_admin.objects.filter(is_deleted=False, school=request.user.school)
            grouped_registers = {}
            for register in registers:
                classroom = register.child_admin.classroom
                student = register.child_admin
                if classroom not in grouped_registers:
                    grouped_registers[classroom] = {}
                if student not in grouped_registers[classroom]:
                    grouped_registers[classroom][student] = []
                grouped_registers[classroom][student].append(register)

            context = {'grouped_registers': grouped_registers}
            return render(request, 'applications-from-classroom-teachers/register_classroom_admin.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        register_id = request.POST.get('register_id')
        register = get_object_or_404(Register_admin, id=register_id, school=request.user.school)
        register.is_deleted = True
        register.save()
        return redirect('register:applications-from-classroom-teachers')


class AddRegister(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            classrooms = Classroom.objects.filter(school=request.user.school)
            context = {
                'classrooms': classrooms,
            }
            return render(request, 'add_register.html', context)
        else:
            return HttpResponseForbidden()

    @transaction.atomic
    def post(self, request):
        if request.user.is_admin:
            classroom_id = request.POST.get('classroom')
            student_id = request.POST.get('student')
            olympiad_id = request.POST.get('olympiad')

            if not classroom_id or not student_id or not olympiad_id:
                return HttpResponseForbidden("Missing data")

            classroom = get_object_or_404(Classroom, id=classroom_id, school=request.user.school)
            student = get_object_or_404(User, id=student_id, classroom=classroom)
            olympiad = get_object_or_404(Olympiad, id=olympiad_id)

            Register_admin.objects.create(
                child_admin=student,
                Olympiad_admin=olympiad,
                teacher_admin=classroom.teacher,
                school=request.user.school
            )

            return redirect('register:applications-from-classroom-teachers')
        else:
            return HttpResponseForbidden()


class TeacherRecommendationsView(TeacherRequiredMixin, View):
    def get(self, request):
        if request.user.is_teacher:
            recommendations = Recommendation.objects.filter(recommended_by=request.user)
            context = {
                'recommendations': recommendations,
            }
            return render(request, 'recommendations/recommendations.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if request.user.is_teacher:
            recommendation_id = request.POST.get('recommendation_id')
            action = request.POST.get('action')
            try:
                recommendation = Recommendation.objects.get(id=recommendation_id, recommended_by=request.user)
                if action == 'delete':
                    recommendation.delete()
                    return HttpResponseRedirect(request.path_info)
            except Recommendation.DoesNotExist:
                return HttpResponseForbidden("Recommendation not found.")
        return HttpResponseForbidden()


class GetStudentsForClassroomView(LoginRequiredMixin, View):
    def get(self, request):
        classroom_id = request.GET.get('classroom_id')
        if classroom_id:
            students = User.objects.filter(classroom__id=classroom_id, is_child=True, school=request.user.school)
            students_data = [{'id': student.id, 'name': student.get_full_name()} for student in students]
            return JsonResponse({'students': students_data})
        else:
            return JsonResponse({'students': []})


class GetOlympiadsForStudentView(LoginRequiredMixin, View):
    def get(self, request):
        student_id = request.GET.get('student_id')
        if student_id:
            student = get_object_or_404(User, pk=student_id, is_child=True, school=request.user.school)
            olympiads = Olympiad.objects.filter(class_olympiad=student.classroom.number)
            olympiads_data = [
                {
                    'id': olympiad.id,
                    'name': olympiad.name,
                    'stage': olympiad.stage.name,
                    'class_olympiad': olympiad.class_olympiad
                }
                for olympiad in olympiads
            ]
            return JsonResponse({'olympiads': olympiads_data})
        else:
            return JsonResponse({'olympiads': []})
