# result/views.py

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import ListView
from django_filters.views import FilterView
from .models import Result
from .filters import ResultFilter
from .forms import OlympiadResultForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import *
from users.models import *
from result.models import *
from register.models import *
from .forms import OlympiadResultClassForm
from users.models import User
from users.mixins import AdminRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from main.models import Classroom
from django.utils.timezone import make_naive
import io


class ExportResultsView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseForbidden()

        results = Result.objects.filter(info_children__school=request.user.school).select_related(
            'info_children__classroom', 'info_olympiad')

        data = []
        for result in results:
            user = result.info_children
            classroom = user.classroom
            olympiad = result.info_olympiad
            data.append({
                'ФИО': user.get_full_name(),
                'Класс': f"{classroom.number} {classroom.letter}" if classroom else 'Нет данных',
                'Название олимпиады': olympiad.name,
                'Количество очков': result.points,
                'Статус результата': result.get_status_result_display(),
                'Дата добавления': result.date_added
            })

        df = pd.DataFrame(data)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Results')

        buffer.seek(0)
        response = HttpResponse(buffer,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=results.xlsx'
        return response


class ImportResultsView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseForbidden()

        users = User.objects.filter(school=request.user.school)
        olympiads = Olympiad.objects.filter(school=request.user.school)
        return render(request, 'result/result.html', {'users': users, 'olympiads': olympiads})

    def post(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseForbidden()

        excel_file = request.FILES.get('excel_file')
        if not excel_file:
            return render(request, 'result/result.html', {'error': 'Файл не выбран'})

        df = pd.read_excel(excel_file)
        errors = []

        for index, row in df.iterrows():
            last_name, first_name, surname = row['Фамилия'], row['Имя'], row['Отчество']
            try:
                user = User.objects.get(
                    last_name=last_name,
                    first_name=first_name,
                    surname=surname,
                    school=request.user.school
                )
            except MultipleObjectsReturned:
                users = User.objects.filter(
                    last_name=last_name,
                    first_name=first_name,
                    surname=surname,
                    school=request.user.school
                )
                user = users.first()
                errors.append(
                    f'Найдено несколько пользователей с именем {last_name} {first_name} {surname}. Использован первый найденный.')

            try:
                olympiad = Olympiad.objects.get(name=row['Название олимпиады'], school=request.user.school)
            except ObjectDoesNotExist:
                errors.append(f'Олимпиада с названием {row["Название олимпиады"]} не найдена.')
                continue

            Result.objects.update_or_create(
                info_children=user,
                info_olympiad=olympiad,
                defaults={
                    'points': row['Количество очков'],
                    'status_result': row['Статус результата'],
                }
            )

        if errors:
            return render(request, 'result/result.html', {'errors': errors})

        return redirect('result:results_list')


class ResultListView(ListView):
    model = Result
    template_name = 'result/result.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(info_children__school=self.request.user.school)
        self.filterset = ResultFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class OlympiadResultCreateView(View):
    def get(self, request):
        form = OlympiadResultForm()
        return render(request, 'olympiad_result_list/olympiad_result_form.html', {'form': form})

    def post(self, request):
        form = OlympiadResultForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            olympiad = form.cleaned_data['olympiad']
            score = form.cleaned_data['score']
            status = form.cleaned_data['status']

            Result.objects.create(
                info_children=student,
                info_olympiad=olympiad,
                points=score,
                status_result=status
            )

            return redirect('result:results_list')
        return render(request, 'olympiad_result_list/olympiad_result_form.html', {'form': form})


class GetOlympiadsView(View):
    def get(self, request):
        student_id = request.GET.get('student_id')
        olympiad_ids = Register_admin.objects.filter(child_admin_id=student_id, school=request.user.school).values_list(
            'Olympiad_admin_id', flat=True)
        olympiads = Olympiad.objects.filter(id__in=olympiad_ids, school=request.user.school)
        olympiad_list = [{'id': olympiad.id, 'name': olympiad.name} for olympiad in olympiads]
        return JsonResponse(olympiad_list, safe=False)


class OlympiadResultClassCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = OlympiadResultClassForm()
        return render(request, 'olympiad_result_class_form/olympiad_result_class_form.html',
                      {'form': form, 'students': []})

    def post(self, request):
        form = OlympiadResultClassForm(request.POST)
        if form.is_valid():
            classroom = form.cleaned_data['classroom']
            olympiad = form.cleaned_data['olympiad']
            score = request.POST.getlist('score')
            status = request.POST.getlist('status')

            for idx, student in enumerate(classroom.child.all()):
                Result.objects.create(
                    info_children=student,
                    info_olympiad=olympiad,
                    points=score[idx],
                    status_result=status[idx]
                )

            return redirect('success_page')
        students = form.cleaned_data['classroom'].child.all() if 'classroom' in form.cleaned_data else []
        return render(request, 'olympiad_result_class_form/olympiad_result_class_form.html',
                      {'form': form, 'students': students})


class GetStudentsView(View):
    def get(self, request):
        classroom_id = request.GET.get('classroom_id')
        if classroom_id:
            classroom = get_object_or_404(Classroom, id=classroom_id, school=request.user.school)
            students = classroom.child_set.filter(
                id__in=Register_admin.objects.filter(school=request.user.school).values_list('child_admin_id',
                                                                                             flat=True))
            html = render_to_string('students_list/students_list.html', {'students': students})
            return JsonResponse({'html': html})
        return JsonResponse({'html': ''})


class StudentResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'student_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Result.objects.filter(info_children=self.request.user, info_children__school=self.request.user.school)
