from rest_framework import serializers
from main.models import Olympiad


class OlympiadSerializer(serializers.ModelSerializer):
    stage = serializers.CharField(source='stage.name')
    class_olympiad = serializers.IntegerField()

    class Meta:
        model = Olympiad
        fields = ['id', 'name', 'stage', 'class_olympiad']
