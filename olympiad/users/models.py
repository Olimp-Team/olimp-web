from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Модель пользователей
    """Пример: Иваницкий Илья Олегович
    Изображение
    29.11.2007
    Ученик
    Пол мужской"""

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    class Gender(models.TextChoices):
        MALE = 'М'
        WOMENS = 'Ж'

    # Общие сведения
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    surname = models.CharField(
        "Отчество пользователя (при наличии)", max_length=256, blank=True, null=True
    )
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    gender = models.CharField("Пол учителя", max_length=2, choices=Gender.choices, default=Gender.MALE)

    def get_types(self):
        return self.Gender

    # Роль пользователя в системе
    is_teacher = models.BooleanField("Учитель", default=False, blank=True,
                                     null=True)  # null ИЗМЕНИТЬ НА FALSE когда будет страница регистрации
    is_child = models.BooleanField("Ученик", default=False, blank=True,
                                   null=True)  # null ИЗМЕНИТЬ НА FALSE когда будет страница регистрации
    is_admin = models.BooleanField("Администратор",
                                   default=False, blank=True,
                                   null=True)  # null ИЗМЕНИТЬ НА FALSE когда будет страница регистрации

    # Сведения для учителей
    classroom_guide = models.ForeignKey('main.Classroom', related_name='classroom_teachers', blank=True,
                                        on_delete=models.CASCADE, null=True)
    subject = models.ManyToManyField(to="main.Subject", verbose_name="Какой предмет ведёт учитель", blank=True)
    post_job_teacher = models.ManyToManyField(to="main.Post", verbose_name="Должность учителя", blank=True)

    # Сведения для учеников
    classroom = models.ForeignKey(to='main.Classroom', on_delete=models.CASCADE, verbose_name='Класс ученика',
                                  blank=True, null=True)

    def __str__(self):
        if self.is_teacher:
            return f"Учитель: {self.last_name} {self.first_name} {self.surname}"
        elif self.is_admin:
            return f"Администратор: {self.last_name} {self.first_name} {self.surname}"
        elif self.is_child:
            return f"{self.last_name} {self.first_name} {self.surname}"
        else:
            return f"Неизвстная роль: {self.last_name} {self.first_name} {self.surname}"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.surname}"

    @staticmethod
    def get_teachers():
        return User.objects.filter(is_teacher=True)

    @staticmethod
    def get_children():
        return User.objects.filter(is_child=True)
