from rest_framework import serializers
from main.models import Olympiad


class OlympiadSerializer(serializers.ModelSerializer):
    # Поле stage будет отображать имя этапа олимпиады
    stage = serializers.CharField(source='stage.name')

    # Поле class_olympiad будет отображать класс олимпиады

    class Meta:
        model = Olympiad
        fields = ['id', 'name', 'stage', 'class_olympiad']  # Поля, которые будут сериализоваться
