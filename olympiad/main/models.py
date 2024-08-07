from django.db import models


class AuditLog(models.Model):
    """
    Модель для ведения журнала аудита действий пользователей.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.CharField(max_length=256, verbose_name='Действие')
    object_name = models.CharField(max_length=256, verbose_name='Объект')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время действия')
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа',
                               related_name='school_audit')

    def __str__(self):
        return f'{self.user} - {self.action} - {self.object_name}'


class Subject(models.Model):
    """
    Модель учебных предметов. Пример: Информатика.
    """

    class Meta:
        verbose_name_plural = "Школьные предметы"
        verbose_name = 'Школьный предмет'

    name = models.CharField('Название школьного предмета', max_length=256, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель категорий олимпиад. Пример: ВСОШ.
    """

    class Meta:
        verbose_name_plural = "Категории олимпиад"
        verbose_name = 'Категория олимпиад'

    name = models.CharField('Название категории', max_length=256)

    def __str__(self):
        return self.name


class LevelOlympiad(models.Model):
    """
    Модель уровней олимпиад. Пример: Муниципальный.
    """

    class Meta:
        verbose_name_plural = "Уровень олимпиад"
        verbose_name = 'Уровень олимпиад'

    name = models.CharField('Название уровня', max_length=256)

    def __str__(self):
        return self.name


class Stage(models.Model):
    """
    Модель этапов олимпиад. Пример: Школьный.
    """

    class Meta:
        verbose_name_plural = "Этапы олимпиад"
        verbose_name = 'Этап олимпиады'

    name = models.CharField('Название категории', max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Модель должностей персонала школы. Пример: Учитель.
    """

    class Meta:
        verbose_name_plural = "Должности"
        verbose_name = 'Должность'

    name = models.CharField('Должность', max_length=512)

    def __str__(self):
        return self.name


class Olympiad(models.Model):
    """
    Модель олимпиады.
    """

    class Meta:
        verbose_name_plural = "Олимпиады"
        verbose_name = 'Олимпиада'

    name = models.CharField('Название олимпиады', max_length=256)
    description = models.TextField('Описание олимпиады', blank=True, null=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Категория олимпиады')
    level = models.ForeignKey(to='LevelOlympiad', on_delete=models.CASCADE, verbose_name='Название уровня')
    stage = models.ForeignKey(to='Stage', on_delete=models.CASCADE, verbose_name='Название этапа')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name='Название школьного предмета')
    class_olympiad = models.IntegerField('Класс олимпиады')
    date = models.DateField('Дата проведения', blank=True, null=True)
    time = models.TimeField('Время проведения', blank=True, null=True)
    location = models.CharField('Место проведения олимпиады', max_length=256, blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.stage} - {self.subject} {self.class_olympiad}'
