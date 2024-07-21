from django.db import models
from users.models import User


class Register(models.Model):
    """Модель заявки учеников
        Иваницкий Илья Олегович - 10 А
        ВСОШ по информатике
        Дата создания заявки - 29.02.24 - 10:15"""

    class Meta:
        verbose_name_plural = 'Заявки регистрации на олимпиады'
        verbose_name = 'Заявка регистрации на олимпиаду'

    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа', related_name='school_register')
    teacher = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='', blank=True, null=True)
    child = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='Ученик')
    Olympiad = models.ForeignKey('main.Olympiad', on_delete=models.CASCADE)
    status_send = models.BooleanField(default=False)

    def __str__(self):
        return (f'ID {self.id}  ФИО {self.child.last_name} {self.child.first_name} {self.child.surname}'
                f' | Олимпиада: {self.Olympiad.name} Статус Ученик: {self.status_send}')


class Register_send(models.Model):
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа', related_name='school_register_send')
    teacher_send = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='teacher_send')
    child_send = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child_send')
    Olympiad_send = models.ForeignKey('main.Olympiad', on_delete=models.CASCADE, related_name='Olympiad_send')
    status_teacher = models.BooleanField(default=False)
    status_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    status_send = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher_send', 'child_send', 'Olympiad_send')

    def __str__(self):
        return f' | Статус Учитель: {self.status_teacher}'


class Register_admin(models.Model):
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа', related_name='school_register_admin')
    teacher_admin = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='teacher_admin')
    child_admin = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='child_admin')
    Olympiad_admin = models.ForeignKey('main.Olympiad', on_delete=models.CASCADE, related_name='Olympiad_admin')
    status_admin = models.BooleanField(default=False)
    status_teacher = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f' | Статус Админ: {self.status_admin}'


class Recommendation(models.Model):
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа', related_name='school_recommendation')
    recommended_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recommendations_by')
    recommended_to = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recommendations_to')
    child = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recommendations_for')
    Olympiad = models.ForeignKey('main.Olympiad', on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  # Принята ли рекомендация классным руководителем

    class Meta:
        unique_together = ('recommended_by', 'recommended_to', 'child', 'Olympiad')

    def __str__(self):
        return f'Recommendation from {self.recommended_by} to {self.recommended_to} for {self.child} to join {self.Olympiad}'
