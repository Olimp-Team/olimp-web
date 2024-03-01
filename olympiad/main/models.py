import uuid
from django.db import models
from users.models import Users


class Classroom(models.Model):
    """Модель учебных классов
    Пример: 10 А - Иваницкий Илья Олегович"""
    class Meta:
        verbose_name_plural = "Учебные классы"
        verbose_name = 'Учебный класс'

    number = models.IntegerField('Цифра', blank=True, null=True)
    letter = models.CharField('Буква', max_length=1, blank=True, null=True)
    info_teacher = models.ForeignKey(to='main.Teacher', blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='info_teacher')

    def __str__(self):
        return f'{self.number} {self.letter} - {self.info_teacher}'


class Subject(models.Model):
    """Модель учебных предметов
    Пример: Информатика"""
    class Meta:
        verbose_name_plural = "Школьные предметы"
        verbose_name = 'Школьный предмет'

    name = models.CharField('Название школьного предмета', max_length=256, unique=True)

    def __str__(self):
        return self.name


class Сategory(models.Model):
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


class Teacher(Users):
    """Модель учителей
    Пример: teacher:732301papa
    Иваницкий Илья Олегович
    icw20@mail.ru
    Работает
    В сети
    Классное руководствое: 10 А"""
    class Meta:
        verbose_name_plural = "Учителя"
        verbose_name = 'Учитель'

    classroom_guide = models.ForeignKey(to="Classroom", on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Классное руководство")
    subject = models.ManyToManyField(to="Subject", verbose_name="Какой предмет ведёт учитель", blank=True)
    post_job_teacher = models.ManyToManyField(to="Post", verbose_name="Должность учителя")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="USER_TEACHER")

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'


class Child(Users):
    """Модель учеников
        Пример: children:732301papa
        Иваницкий Илья Олегович
        icw20@mail.ru
        Учится
        В сети
        Учебный класс: 10 А"""
    class Meta:
        verbose_name_plural = "Ученики"
        verbose_name = 'Ученик'

    classroom = models.ForeignKey(to='Classroom', on_delete=models.CASCADE, verbose_name='Класс ученика',
                                  blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="USER_CHILD")

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'


class Admin(Users):
    """Модель администратора
        Пример: admin:732301papa
        Иваницкий Илья Олегович
        icw20@mail.ru
        Работает
        В сети"""
    class Meta:
        verbose_name_plural = "Администраторы"
        verbose_name = 'Администратор'

    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="USER_ADMIN")


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
    category = models.ForeignKey(to='Сategory', on_delete=models.CASCADE, verbose_name='Категория олимпиады',
                                 max_length=256)
    level = models.ForeignKey(to='Level_olympiad', on_delete=models.CASCADE, verbose_name='Название уровня',
                              max_length=256)
    stage = models.ForeignKey(to='Stage', on_delete=models.CASCADE, verbose_name='Название этапа', max_length=256)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Название школьного предмета')
    class_olympiad = models.IntegerField('Класс олимпиады')
    date_olympiad = models.DateTimeField('Дата проведения олимпиады')

    # locations = models.CharField(verbose_name='Место проведения олимпиады')
    def __str__(self):
        return f'{self.name} {self.category} {self.level} {self.stage} {self.subject} {self.class_olympiad} {self.date_olympiad}'


class Register(models.Model):
    """Модель заявки учеников
        Иваницкий Илья Олегович - 10 А
        ВСОШ по информатике
        Дата создания заявки - 29.02.24 - 10:15"""
    class Meta:
        verbose_name_plural = 'Заявки регистрации на олимпиады'
        verbose_name = 'Заявка регистрации на олимпиаду'

    user = models.ForeignKey(to="users.Users", on_delete=models.CASCADE)
    Olympiad = models.ForeignKey(to='Olympiad', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'ID {self.id}  ФИО {self.user.last_name} {self.user.first_name} {self.user.surname}'
                f' | Олимпиада: {self.Olympiad.name}')


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
    info_children = models.ForeignKey(to="Child", on_delete=models.CASCADE,
                                      verbose_name='Информация об ученике')
    info_olympiad = models.ForeignKey(to='Olympiad', on_delete=models.CASCADE, verbose_name='Информация об олимпиаде')
    points = models.IntegerField(verbose_name='Количество намбранных очков')
    status_result = models.CharField(verbose_name='Статус результата', max_length=256, choices=STATUSRES,
                                     default=PARTICIPANT)
    date_results = models.DateTimeField()


