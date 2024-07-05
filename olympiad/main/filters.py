import django_filters
from .models import Olympiad


class OlympiadFilter(django_filters.FilterSet):
    class Meta:
        model = Olympiad
        fields = {
            'date': ['exact'],
            'category': ['exact'],
            'stage': ['exact'],
        }
