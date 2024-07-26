from django.db import models
from datetime import datetime


class Classroom(models.Model):
    number = models.IntegerField('Цифра', blank=True, null=True)
    letter = models.CharField('Буква', max_length=1, blank=True, null=True)
    teacher = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.CASCADE, related_name='teacher')
    child = models.ManyToManyField('users.User', blank=True, related_name='Child')
    is_graduated = models.BooleanField('Выпустился', default=False)
    graduation_year = models.IntegerField('Год выпуска', blank=True, null=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа',
                               related_name='school_classroom')

    def __str__(self):
        return f'{self.number} {self.letter} - {self.teacher}'

    def promote(self):
        if self.number < 11:
            self.number += 1
        else:
            self.is_graduated = True
            self.graduation_year = datetime.now().year
        self.save()
