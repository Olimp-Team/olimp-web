from django.db import models


class School(models.Model):
    """
    Модель, представляющая школу с основными контактными данными.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название школы', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True, null=True)
    region = models.CharField(max_length=100, verbose_name='Субъект РФ', blank=True, null=True)
    locality = models.CharField(max_length=100, verbose_name='Населенный пункт', blank=True, null=True)
    principal_name = models.CharField(max_length=255, verbose_name='Директор', blank=True, null=True)
    contact_email = models.EmailField(verbose_name='Контактный email', blank=True, null=True)
    contact_phone = models.CharField(max_length=20, verbose_name='Контактный телефон', blank=True, null=True)
    domain = models.CharField(max_length=255, verbose_name='Домен', blank=True, null=True)
    website = models.URLField(blank=True, null=True, verbose_name='Веб-сайт')
    established_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год основания')
    number_of_students = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество учащихся')
    school_type = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('public', 'Государственная'),
        ('private', 'Частная'),
        ('charter', 'Чартерная')
    ], verbose_name='Тип школы')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True, verbose_name='Логотип')

    # Контактная информация заявителя
    applicant_name = models.CharField(max_length=255, verbose_name='ФИО заполнителя заявки', blank=True, null=True)
    applicant_phone = models.CharField(max_length=20, verbose_name='Телефон заполнителя заявки', blank=True, null=True)
    applicant_email = models.EmailField(verbose_name='E-mail заполнителя заявки', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'
