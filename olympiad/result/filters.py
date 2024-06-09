import django_filters
from main.models import *
from register.models import *
from result.models import *
from users.models import User

class ResultFilter(django_filters.FilterSet):
    classroom = django_filters.ModelChoiceFilter(
        field_name='info_children__classroom',
        queryset=Classroom.objects.all(),
        label='Класс'
    )
    olympiad = django_filters.ModelChoiceFilter(
        field_name='info_olympiad',
        queryset=Olympiad.objects.all(),
        label='Олимпиада'
    )

    class Meta:
        model = Result
        fields = ['classroom', 'olympiad']
