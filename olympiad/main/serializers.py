from rest_framework import serializers

from users.models import Users


class UsersSerializer(serializers.ModelSerializer):
    """API Пользователей"""
    class Meta:
        model = Users
        fields = '__all__'
