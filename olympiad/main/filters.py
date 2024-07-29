import django_filters
from .models import Olympiad

class OlympiadFilter(django_filters.FilterSet):
    """
    Фильтр для модели Olympiad.
    Позволяет фильтровать олимпиады по дате, категории и этапу.
    """
    class Meta:
        model = Olympiad
        fields = {
            'date': ['exact'],          # Фильтрация по точной дате
            'category': ['exact'],      # Фильтрация по точной категории
            'stage': ['exact'],         # Фильтрация по точному этапу
        }
