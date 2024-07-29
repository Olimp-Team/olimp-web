from django.db import models
from users.models import User
from main.models import Olympiad
from school.models import School


class Register(models.Model):
    """Модель заявки учеников на олимпиады"""

    class Meta:
        verbose_name_plural = 'Заявки регистрации на олимпиады'
        verbose_name = 'Заявка регистрации на олимпиаду'

    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа', related_name='school_register')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель', blank=True, null=True)
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Ученик')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    status_send = models.BooleanField(default=False, verbose_name='Статус отправки')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return (f'ID {self.id} ФИО {self.child.last_name} {self.child.first_name} {self.child.surname} | '
                f'Олимпиада: {self.olympiad.name} Статус отправки: {self.status_send}')

    objects = models.Manager()


class RegisterSend(models.Model):
    """Модель отправки заявки ученика на олимпиаду учителем"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа',
                               related_name='school_register_send', null=True, blank=True)
    teacher_send = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель отправитель')
    child_send = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_send')
    olympiad_send = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='olympiad_send')
    status_teacher = models.BooleanField(default=False, verbose_name='Статус учителя')
    status_admin = models.BooleanField(default=False, verbose_name='Статус администратора')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')
    status_send = models.BooleanField(default=False, verbose_name='Статус отправки')

    class Meta:
        unique_together = ('teacher_send', 'child_send', 'olympiad_send')

    def __str__(self):
        return f'Статус учителя: {self.status_teacher}'

    objects = models.Manager()


class RegisterAdmin(models.Model):
    """Модель утверждения заявки администраторами"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='Школа',
                               related_name='school_register_admin')
    teacher_admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Учитель администратор')
    child_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_admin')
    olympiad_admin = models.ForeignKey(Olympiad, on_delete=models.CASCADE, related_name='olympiad_admin')
    status_admin = models.BooleanField(default=False, verbose_name='Статус администратора')
    status_teacher = models.BooleanField(default=False, verbose_name='Статус учителя')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return f'Статус администратора: {self.status_admin}'

    objects = models.Manager()


class Recommendation(models.Model):
    """Модель рекомендаций для участия в олимпиадах"""
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    STATUS_CHOICES = [
        (PENDING, 'В ожидании'),
        (ACCEPTED, 'Принято'),
        (DECLINED, 'Отказано учеником'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_recommendation')
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_by')
    recommended_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_to')
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_for')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, verbose_name='Статус')

    class Meta:
        unique_together = ('recommended_by', 'recommended_to', 'child', 'olympiad')

    def __str__(self):
        return f'Рекомендация от {self.recommended_by} для {self.recommended_to} для участия {self.child} в {self.olympiad}'

    objects = models.Manager()
