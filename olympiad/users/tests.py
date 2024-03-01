from django.test import TestCase
from models import *

# Смена пароля Пользователя
a = Users.objects.get(username=input('Введите логин'))
a.set_password(input('Новый пароль'))
a.save()
