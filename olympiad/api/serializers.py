from rest_framework import serializers
from users.models import User
from main.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class СategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Сategory
        fields = '__all__'


class Level_olympiadSerializer(serializers.ModelSerializer):
    """API Пользователей"""

    class Meta:
        model = Level_olympiad
        fields = '__all__'


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class OlympiadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Olympiad
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class Register_sendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register_send
        fields = '__all__'


class Register_adminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register_admin
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
