from django.test import TestCase

from main.models import Olympiad

for olympiad in Olympiad.objects.all():
    print(olympiad.name, olympiad.stage, olympiad.class_olympiad)