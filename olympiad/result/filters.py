import django_filters
from main.models import *
from register.models import *
from result.models import *
from django import forms
import django_filters


class ResultFilter(django_filters.FilterSet):
    classroom = django_filters.ModelChoiceFilter(
        field_name='info_children__classroom',
        queryset=Classroom.objects.filter(
            id__in=Register_admin.objects.values_list('child_admin__classroom_id', flat=True).distinct()
        ),
        label='Класс',
        widget=forms.Select(attrs={'class': 'block w-full mt-1 p-2 border rounded classroom-select'})
    )
    olympiad = django_filters.ModelChoiceFilter(
        field_name='info_olympiad',
        queryset=Olympiad.objects.filter(
            id__in=Register_admin.objects.values_list('Olympiad_admin_id', flat=True).distinct()
        ),
        label='Олимпиада',
        widget=forms.Select(attrs={'class': 'block w-full mt-1 p-2 border rounded olympiad-select'})
    )

    class Meta:
        model = Result
        fields = ['classroom', 'olympiad']
