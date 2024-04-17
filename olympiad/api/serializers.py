from rest_framework import serializers
from users.models import User
from main.models import *


class ChildrenApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



    # def validate(self, data):
    #     if data['username'] == self.context['request'].user:
    #         raise serializers.ValidationError('Logged in User is not an Author')
    #     return data

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'
