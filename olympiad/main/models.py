from django.db import models

from datetime import datetime


class Classroom(models.Model):
    """Модель учебных классов
    Пример: 10 А - Иваницкий Илья Олегович"""

    class Meta:
        verbose_name_plural = "Учебные классы"
        verbose_name = 'Учебный класс'

    number = models.IntegerField('Цифра', blank=True, null=True)
    letter = models.CharField('Буква', max_length=1, blank=True, null=True)
    teacher = models.ForeignKey(to='users.User', blank=True, null=True, on_delete=models.CASCADE,
                                related_name='teacher')
    child = models.ManyToManyField(to='users.User', blank=True, related_name='Child')
    is_graduated = models.BooleanField('Выпустился', default=False)
    graduation_year = models.IntegerField('Год выпуска', blank=True, null=True)

    def __str__(self):
        return f'{self.number} {self.letter} - {self.teacher}'

    def promote(self):
        if self.number < 11:
            self.number += 1
        else:
            self.is_graduated = True
            self.graduation_year = datetime.now().year
        self.save()


class AuditLog(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.CharField(max_length=256, verbose_name='Действие')
    object_name = models.CharField(max_length=256, verbose_name='Объект')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время действия')

    def __str__(self):
        return f'{self.user} - {self.action} - {self.object_name} - {self.timestamp}'


class Subject(models.Model):
    """Модель учебных предметов
    Пример: Информатика"""

    class Meta:
        verbose_name_plural = "Школьные предметы"
        verbose_name = 'Школьный предмет'

    name = models.CharField('Название школьного предмета', max_length=256, unique=True)

    def __str__(self):
        return self.name


class categories(models.Model):
    """Модель категорий олимпиад
    Пример: ВСОШ"""

    class Meta:
        verbose_name_plural = "Категории олимпиад"
        verbose_name = 'Категория олимпиад'

    name = models.CharField('Название категории', max_length=256)

    def __str__(self):
        return self.name


class Level_olympiad(models.Model):
    """Модель уровней олимпиад
    Пример: Муницыпальный"""

    class Meta:
        verbose_name_plural = "Уровень олимпиад"
        verbose_name = 'Уровень олимпиад'

    name = models.CharField('Название уровня', max_length=256)

    def __str__(self):
        return self.name


class Stage(models.Model):
    """Модель этапов олимпиад
    Пример: Школьный"""

    class Meta:
        verbose_name_plural = "Этапы олимпиад"
        verbose_name = 'Этап олимпиады'

    name = models.CharField('Название категории', max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель должностей персонала школы
    Пример: Учитель"""

    class Meta:
        verbose_name_plural = "Должности"
        verbose_name = 'Должность'

    name = models.CharField('Должность', max_length=512)

    def __str__(self):
        return self.name


from django.db import models


class Olympiad(models.Model):
    """Модель олимпиады"""

    class Meta:
        verbose_name_plural = "Олимпиады"
        verbose_name = 'Олимпиада'

    name = models.CharField('Название олимпиады', max_length=256)
    description = models.TextField('Описание олимпиады', blank=True, null=True)
    category = models.ForeignKey(to='categories', on_delete=models.CASCADE, verbose_name='Категория олимпиады',
                                 max_length=256)
    level = models.ForeignKey(to='Level_olympiad', on_delete=models.CASCADE, verbose_name='Название уровня',
                              max_length=256)
    # next_stage = models.ForeignKey('Stage', on_delete=models.SET_NULL, null=True, blank=True,
    #                                related_name='next_olympiads', verbose_name='Следующий этап')
    stage = models.ForeignKey(to='Stage', on_delete=models.CASCADE, verbose_name='Название этапа', max_length=256)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Название школьного предмета')
    class_olympiad = models.IntegerField('Класс олимпиады')
    date = models.DateField('Дата проведения')
    time = models.TimeField('Время проведения')
    location = models.CharField('Место проведения олимпиады', max_length=256)

    def __str__(self):
        return f'{self.name} {self.category} {self.level} {self.stage} {self.subject} {self.class_olympiad}'
