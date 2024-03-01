from django.test import TestCase
from models import *

# Смена пароля Учителя
a = Teacher.objects.get(username=input('Введите логин'))
a.set_password(input('Новый пароль'))
a.save()
# Смена пароля Ученика
b = Child.objects.get(username=input('Введите логин'))
b.set_password(input('Новый пароль'))
b.save()
# Смена пароля Администратора
c = Admin.objects.get(username=input('Введите логин'))
c.set_password(input('Новый пароль'))
c.save()
