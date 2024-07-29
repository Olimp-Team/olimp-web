from django.db import models
from django.contrib.auth.models import AbstractUser
from image_cropping import ImageRatioField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from school.models import School
from classroom.models import Classroom


class User(AbstractUser):
    """
    Расширенная модель пользователя, включающая дополнительные поля для различных ролей и информации о пользователе.
    """
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    image = ProcessedImageField(
        upload_to='users_images',
        processors=[ResizeToFill(150, 150)],
        format='JPEG',
        options={'quality': 90},
        null=True, blank=True
    )
    cropping = ImageRatioField('image', '300x300')
    surname = models.CharField(
        "Отчество пользователя (при наличии)", max_length=256, blank=True, null=True
    )
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    gender = models.CharField("Пол", max_length=2, choices=GENDER_CHOICES)
    telegram_id = models.CharField(max_length=64, blank=True, null=True, verbose_name="Telegram ID")

    is_teacher = models.BooleanField("Учитель", default=False, blank=True, null=True)
    is_child = models.BooleanField("Ученик", default=False, blank=True, null=True)
    is_admin = models.BooleanField("Администратор", default=False, blank=True, null=True)

    is_expelled = models.BooleanField("Исключен", default=False, blank=True, null=True)

    classroom_guide = models.ForeignKey('classroom.Classroom', related_name='classroom_teachers', blank=True,
                                        on_delete=models.CASCADE, null=True)
    subject = models.ManyToManyField(to="main.Subject", verbose_name="Какой предмет ведёт учитель",
                                     blank=True)
    post_job_teacher = models.ManyToManyField(to="main.Post", verbose_name="Должность учителя",
                                              blank=True)

    classroom = models.ForeignKey(to='classroom.Classroom', on_delete=models.CASCADE, verbose_name='Класс ученика',
                                  blank=True, null=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name='users',
                               blank=True, null=True)

    def __str__(self):
        """
        Возвращает строковое представление пользователя в зависимости от его роли.
        """
        if self.is_teacher:
            return f"Учитель: {self.last_name} {self.first_name} {self.surname}"
        elif self.is_admin:
            return f"Администратор: {self.last_name} {self.first_name} {self.surname}"
        elif self.is_child:
            return f"{self.last_name} {self.first_name} {self.surname}"
        else:
            return f"Неизвестная роль: {self.last_name} {self.first_name} {self.surname}"

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        full_name = f"{self.last_name} {self.first_name} {self.surname}"
        return full_name.strip()

    @staticmethod
    def get_teachers():
        """
        Возвращает QuerySet всех пользователей с ролью учителя.
        """
        return User.objects.filter(is_teacher=True)

    @staticmethod
    def get_children():
        """
        Возвращает QuerySet всех пользователей с ролью ученика.
        """
        return User.objects.filter(is_child=True)
