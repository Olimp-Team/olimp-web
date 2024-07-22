# register/views.py
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from main.models import *
from register.models import *
from django.views.generic import *
from users.models import User
from users.mixins import AdminRequiredMixin, ChildRequiredMixin, TeacherRequiredMixin


class RegisterPage(ChildRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_child:
            school_stage = Stage.objects.get(name='Школьный')
            olympiads = Olympiad.objects.filter(class_olympiad=request.user.classroom.number, stage=school_stage,
                                                school=request.user.school)
            registered_olympiads = Register_send.objects.filter(child_send=request.user,
                                                                school=request.user.school).values_list(
                'Olympiad_send_id', flat=True)
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
            olympiad = get_object_or_404(Olympiad, id=Olympiad_id, school=request.user.school)
            if olympiad.stage.name != 'Школьный':
                return HttpResponseForbidden('Регистрация возможна только на школьный этап.')

            register, created = Register.objects.update_or_create(
                child=request.user,
                Olympiad=olympiad,
                defaults={'teacher': request.user.classroom.teacher, 'school': request.user.school}
            )

            Register_send.objects.update_or_create(
                teacher_send=request.user.classroom.teacher,
                child_send=request.user,
                Olympiad_send=olympiad,
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

    def post(self, request, *args, **kwargs):
        pass


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
                'recommendations': Recommendation.objects.filter(child=request.user, status=False,
                                                                 school=request.user.school),
                'register_sends': Register_send.objects.filter(child_send=request.user, school=request.user.school),
                'deleted_registers': Register_send.objects.filter(child_send=request.user, is_deleted=True,
                                                                  school=request.user.school),
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

            olympiad = get_object_or_404(Olympiad, id=olympiad_id, school=request.user.school)

            if action == 're-register':
                register, created = Register.objects.update_or_create(
                    child=request.user,
                    Olympiad=olympiad,
                    defaults={'teacher': request.user.classroom.teacher, 'school': request.user.school}
                )

                Register_send.objects.update_or_create(
                    teacher_send=request.user.classroom.teacher,
                    child_send=request.user,
                    Olympiad_send=olympiad,
                    defaults={'is_deleted': False, 'status_send': False, 'status_teacher': False, 'status_admin': False,
                              'school': request.user.school}
                )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
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

            recommendations = Recommendation.objects.filter(recommended_to=request.user, status=False,
                                                            school=request.user.school)
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

    recommendation = get_object_or_404(Recommendation, id=recommendation_id, school=request.user.school)

    Register_send.objects.create(
        teacher_send=request.user,
        child_send=recommendation.child,
        Olympiad_send=recommendation.Olympiad,
        status_send=False,
        is_deleted=False,
        school=request.user.school
    )
    recommendation.status = True
    recommendation.save()

    return redirect('register:student-applications')


def reject_recommendation(request, recommendation_id):
    if not request.user.is_teacher:
        return HttpResponseForbidden()

    recommendation = get_object_or_404(Recommendation, id=recommendation_id, school=request.user.school)
    recommendation.status = True
    recommendation.save()

    return redirect('register:student-applications')


class RegisterDeleteTeacher(TeacherRequiredMixin, View):
    def post(self, request, Olympiad_id, student_id):
        if request.user.is_teacher:
            try:
                register = Register_send.objects.get(Olympiad_send_id=Olympiad_id, child_send_id=student_id,
                                                     is_deleted=False, school=request.user.school)
                register.is_deleted = True
                register.save()

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
            school_stage = Stage.objects.get(name='Школьный')
            context = {
                'students': User.objects.filter(is_child=True, school=request.user.school),
                'olympiads': Olympiad.objects.filter(stage=school_stage, school=request.user.school),
                'teachers': User.objects.filter(is_teacher=True, school=request.user.school)
            }
            return render(request, 'add-recommendation/add-recommendation.html', context)
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if request.user.is_teacher:
            recommended_to = get_object_or_404(User, id=request.POST['recommended_to'], school=request.user.school)
            child = get_object_or_404(User, id=request.POST['child'], school=request.user.school)
            olympiad = get_object_or_404(Olympiad, id=request.POST['olympiad'], school=request.user.school)

            Recommendation.objects.create(
                recommended_by=request.user,
                recommended_to=recommended_to,
                child=child,
                Olympiad=olympiad,
                school=request.user.school
            )
            AuditLog.objects.create(
                user=request.user,
                action='Создание рекомендации',
                object_name=f'Рекомендация ученику {child.get_full_name()} на олимпиаду {olympiad.name}'
            )
            return render(request, 'add-recommendation/add-recommendation.html')
        else:
            return HttpResponseForbidden()


class GetOlympiadsForStudent(View):
    def get(self, request):
        school_stage = Stage.objects.get(name='Школьный')
        student_id = request.GET.get('student_id')
        student = get_object_or_404(User, id=student_id, school=request.user.school)
        olympiads = Olympiad.objects.filter(class_olympiad=student.classroom.number, stage=school_stage,
                                            school=request.user.school)
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

        if not student_id:
            return HttpResponseForbidden("Missing student_id")
        if not recommended_by_id:
            return HttpResponseForbidden("Missing recommended_by_id")
        if not olympiad_id:
            return HttpResponseForbidden("Missing olympiad_id")
        if not action:
            return HttpResponseForbidden("Missing action")

        student = get_object_or_404(User, pk=student_id, school=request.user.school)
        recommended_by = get_object_or_404(User, pk=recommended_by_id, school=request.user.school)
        olympiad = get_object_or_404(Olympiad, pk=olympiad_id, school=request.user.school)

        if action == 'accept':
            Register_send.objects.create(
                teacher_send=request.user,
                child_send=student,
                Olympiad_send=olympiad,
                status_send=False,
                school=request.user.school
            )
            recommendation = get_object_or_404(
                Recommendation,
                recommended_by=recommended_by,
                recommended_to=request.user,
                child=student,
                Olympiad=olympiad,
                school=request.user.school
            )
            recommendation.status = True
            recommendation.save()
        elif action == 'decline':
            Recommendation.objects.filter(
                recommended_by=recommended_by,
                recommended_to=request.user,
                child=student,
                Olympiad=olympiad,
                school=request.user.school
            ).delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class RegisterListClassroom(AdminRequiredMixin, View):
    def get(self, request):
        if request.user.is_admin:
            registers = Register_admin.objects.filter(is_deleted=False, school=request.user.school)
            grouped_registers = {}
            for register in registers:
                classroom = register.child_admin.classroom
                if classroom not in grouped_registers:
                    grouped_registers[classroom] = []
                grouped_registers[classroom].append(register)

            context = {
                'grouped_registers': grouped_registers
            }
            return render(request, 'applications-from-classroom-teachers/register_classroom_admin.html', context)
        else:
            return HttpResponseForbidden()
