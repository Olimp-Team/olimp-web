from django.db import models

class School(models.Model):
    """
    Модель, представляющая школу с основными контактными данными.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название школы')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    contact_email = models.EmailField(verbose_name='Контактный email')
    contact_phone = models.CharField(max_length=20, verbose_name='Контактный телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'
