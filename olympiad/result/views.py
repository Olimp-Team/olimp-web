import pandas as pd
from django.http import HttpResponse
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


class ExportResultsView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        filter_set = ResultFilter(request.GET, queryset=Result.objects.all())
        results = filter_set.qs.values(
            'info_children__last_name',
            'info_children__first_name',
            'info_children__surname',
            'info_olympiad__name',
            'points',
            'status_result',
            'date_added'
        )

        # Создаем DataFrame для экспорта
        df = pd.DataFrame(results)

        # Переименовываем столбцы для удобства
        df.columns = ['Фамилия', 'Имя', 'Отчество', 'Название олимпиады', 'Количество очков', 'Статус результата',
                      'Дата']

        # Преобразуем столбец 'Дата' в неявные объекты datetime без учета часового пояса
        df['Даtта'] = df['Дата'].dt.tz_convert(None)

        # Создаем HTTP-ответ с файлом Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=results.xlsx'

        # Записываем DataFrame в файл Excel
        df.to_excel(response, index=False)

        return response


class ImportResultsView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        olympiads = Olympiad.objects.all()
        return render(request, 'result_list.html', {'users': users, 'olympiads': olympiads})

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            # Получаем отдельные части имени
            last_name, first_name, middle_name = row['Фамилия'], row['Имя'], row['Отчество']
            # Находим или создаем объект User
            user, created = User.objects.get_or_create(
                last_name=last_name,
                first_name=first_name,
                surname=middle_name
            )

            # Находим объект Olympiad по названию
            olympiad = Olympiad.objects.get(name=row['Название олимпиады'])

            # Создаем или обновляем результат
            Result.objects.update_or_create(
                info_children=user,
                info_olympiad=olympiad,
                defaults={
                    'points': row['Количество очков'],
                    'status_result': row['Статус результата'],
                }
            )

        return redirect('results_list')


class ResultListView(FilterView):
    model = Result
    template_name = 'result/result.html'
    context_object_name = 'results'
    filterset_class = ResultFilter


class OlympiadResultCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = OlympiadResultForm()
        return render(request, 'olympiad_result_list/olympiad_result_list.html', {'form': form})

    def post(self, request):
        form = OlympiadResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Замените 'success_page' на ваш URL для успешного добавления
        return render(request, 'olympiad_result_list/olympiad_result_list.html', {'form': form})


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

            return redirect('success_page')  # Замените 'success_page' на ваш URL для успешного добавления
        students = form.cleaned_data['classroom'].child.all() if 'classroom' in form.cleaned_data else []
        return render(request, 'olympiad_result_class_form/olympiad_result_class_form.html',
                      {'form': form, 'students': students})


class get_students(View):
    def get(self, request):
        classroom_id = request.GET.get('classroom_id')
        if classroom_id:
            classroom = Classroom.objects.get(id=classroom_id)
            students = classroom.child.all()
            html = render_to_string('students_list.html', {'students': students})
            return JsonResponse({'html': html})
        return JsonResponse({'html': ''})


class StudentResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'student_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Result.objects.filter(info_children=self.request.user)
