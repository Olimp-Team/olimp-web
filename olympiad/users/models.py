from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser



class Users(AbstractUser):
    # Модель пользователей
    """Пример: Иваницкий Илья Олегович
    Изображение
    29.11.2007
    Ученик
    Пол мужской"""

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    MALE = 'М'
    WOMENS = 'Ж'
    GENDERS = [("М", "Мужчина"), ("Ж", "Женщина")]
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    surname = models.CharField(
        "Отчество пользователя (при наличии)", max_length=256, blank=True, null=True
    )
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    gender = models.CharField("Пол учителя", max_length=1, choices=GENDERS, default=MALE)
    is_teacher = models.BooleanField("Учитель", default=False,
                                     null=True)  # null ИЗМЕНИТЬ НА FALSE когда будет страница регистрации
    is_child = models.BooleanField("Ученик", default=False,
                                   null=True)  # null ИЗМЕНИТЬ НА FALSE когда будет страница регистрации
    is_admin = models.BooleanField("Администратор",
                                   default=False, null=True)  # null ИЗМЕНИТЬ НА FALSE когда будет страница регистрации
    classroom_guide = models.ManyToManyField('main.Child', related_name='classroom_teachers')
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.surname}"
