import django_filters
from django import forms
from main.models import Olympiad
from register.models import RegisterAdmin
from result.models import Result
from classroom.models import Classroom


class ResultFilter(django_filters.FilterSet):
    """
    Фильтр для результатов олимпиад с возможностью фильтрации по классу и олимпиаде.
    """

    # Фильтр по классам, доступным в RegisterAdmin
    classroom = django_filters.ModelChoiceFilter(
        field_name='info_children__classroom',
        queryset=Classroom.objects.filter(
            id__in=RegisterAdmin.objects.values_list('child_admin__classroom_id', flat=True).distinct()
        ),
        label='Класс',
        widget=forms.Select(attrs={'class': 'block w-full mt-1 p-2 border rounded classroom-select'})
    )

    # Фильтр по олимпиадам, доступным в RegisterAdmin
    olympiad = django_filters.ModelChoiceFilter(
        field_name='info_olympiad',
        queryset=Olympiad.objects.filter(
            id__in=RegisterAdmin.objects.values_list('olympiad_admin_id', flat=True).distinct()
        ),
        label='Олимпиада',
        widget=forms.Select(attrs={'class': 'block w-full mt-1 p-2 border rounded olympiad-select'})
    )

    class Meta:
        model = Result
        fields = ['classroom', 'olympiad']
