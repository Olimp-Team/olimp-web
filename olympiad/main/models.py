from django.db import models
from users.models import User


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

    def __str__(self):
        return f'{self.number} {self.letter} - {self.teacher}'


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


class Olympiad(models.Model):
    """Модель олимпиады
        Пример:
        ВСОШ по русскому языку
        Описание
        Мунципальная
        Школьный
        Русский язык
        10 класс
        29.02.2024 - 13:40
        Карла Маркса 153, Школа №53"""
    class Meta:
        verbose_name_plural = "Олимпиады"
        verbose_name = 'Олимпиада'

    name = models.CharField('Название олимпиады', max_length=256)
    description = models.TextField('Описание олимпиады', blank=True, null=True)
    category = models.ForeignKey(to='categories', on_delete=models.CASCADE, verbose_name='Категория олимпиады',
                                 max_length=256)
    level = models.ForeignKey(to='Level_olympiad', on_delete=models.CASCADE, verbose_name='Название уровня',
                              max_length=256)
    stage = models.ForeignKey(to='Stage', on_delete=models.CASCADE, verbose_name='Название этапа', max_length=256)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Название школьного предмета')
    class_olympiad = models.IntegerField('Класс олимпиады')

    # locations = models.CharField(verbose_name='Место проведения олимпиады')
    def __str__(self):
        return f'{self.name} {self.category} {self.level} {self.stage} {self.subject} {self.class_olympiad}'


class Register(models.Model):
    """Модель заявки учеников
        Иваницкий Илья Олегович - 10 А
        ВСОШ по информатике
        Дата создания заявки - 29.02.24 - 10:15"""
    class Meta:
        verbose_name_plural = 'Заявки регистрации на олимпиады'
        verbose_name = 'Заявка регистрации на олимпиаду'

    teacher = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='', blank=True, null=True, )
    child = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name='Ученик')
    Olympiad = models.ForeignKey(to='Olympiad', on_delete=models.CASCADE)
    status_send = models.BooleanField(default=False)

    def __str__(self):
        return (f'ID {self.id}  ФИО {self.child.last_name} {self.child.first_name} {self.child.surname}'
                f' | Олимпиада: {self.Olympiad.name} Статус Ученик: {self.status_send}')


class Register_send(models.Model):
    Register_send_str = models.ForeignKey(to='Register', on_delete=models.CASCADE, related_name='Register')
    status_teacher = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Register_send_str} | Статус Учитель: {self.status_teacher}'


class Register_admin(models.Model):
    Register_admin_str = models.ForeignKey(to='Register_send', on_delete=models.CASCADE, related_name='Register_admin')
    status_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Register_admin_str} | Статус Админ: {self.status_admin}'


class Result(models.Model):
    """Модель результатов учеников
        Иваницкий Илья Олегович
        ВСОШ по Русскому языку
        50/100 баллов
        Участник
        1.03.24"""
    class Meta:
        verbose_name_plural = 'Резльтаты олимпиад'
        verbose_name = 'Результат олимпиады'

    PARTICIPANT = 'У'
    PRIZE = 'ПР'
    WINNER = 'ПОБД'
    STATUSRES = [
        (PARTICIPANT, 'Участник'),
        (PRIZE, 'Призер'),
        (WINNER, 'Победитель')

    ]
    info_children = models.ForeignKey(to="users.User", on_delete=models.CASCADE,
                                      verbose_name='Информация об ученике')
    info_olympiad = models.ForeignKey(to='Olympiad', on_delete=models.CASCADE, verbose_name='Информация об олимпиаде')
    points = models.IntegerField(verbose_name='Количество намбранных очков')
    status_result = models.CharField(verbose_name='Статус результата', max_length=256, choices=STATUSRES,
                                     default=PARTICIPANT)
