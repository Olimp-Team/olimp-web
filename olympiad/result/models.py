from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from raiting_system.models import Rating, Medal


class Result(models.Model):
    """
    Модель для хранения результатов олимпиад.
    """
    PARTICIPANT = 'У'
    PRIZE = 'ПР'
    WINNER = 'ПОБД'

    STATUSRES = [
        (PARTICIPANT, 'Участник'),
        (PRIZE, 'Призер'),
        (WINNER, 'Победитель')
    ]

    info_children = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Информация об ученике')
    info_olympiad = models.ForeignKey('main.Olympiad', on_delete=models.CASCADE, verbose_name='Информация об олимпиаде')
    points = models.PositiveIntegerField(verbose_name='Количество набранных очков', blank=True, null=True)
    status_result = models.CharField(verbose_name='Статус результата', max_length=256, choices=STATUSRES,
                                     default=PARTICIPANT)
    advanced = models.BooleanField(default=False, verbose_name='Прошел на следующий этап')
    date_added = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, verbose_name='Школа')

    def __str__(self):
        return f'{self.info_children} - {self.info_olympiad} - {self.points}'

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для обновления рейтинга пользователя после сохранения результата.
        """
        super().save(*args, **kwargs)
        self.update_user_rating()

    def update_user_rating(self):
        """
        Обновление рейтинга пользователя в зависимости от статуса и этапа олимпиады.
        """
        points = 0
        medal_type = None

        if self.info_olympiad.stage.name == 'Школьный':
            if self.status_result == self.WINNER:
                points = 100
                medal_type = Medal.SILVER
            elif self.status_result == self.PRIZE:
                points = 50
                medal_type = Medal.BRONZE
        elif self.info_olympiad.stage.name == 'Городской':
            if self.status_result == self.WINNER:
                points = 450
                medal_type = Medal.PLATINUM
            elif self.status_result == self.PRIZE:
                points = 300
                medal_type = Medal.GOLD
        elif self.info_olympiad.stage.name == 'Региональный':
            if self.status_result == self.WINNER:
                points = 1000
                medal_type = Medal.RUBY
            elif self.status_result == self.PRIZE:
                points = 450
                medal_type = Medal.PLATINUM
        elif self.info_olympiad.stage.name == 'Заключительный':
            if self.status_result == self.WINNER:
                points = 6000
                medal_type = Medal.PERSONAL
            elif self.status_result == self.PRIZE:
                points = 3000
                medal_type = Medal.DIAMOND

        rating, created = Rating.objects.get_or_create(user=self.info_children)
        rating.update_points(points)

        if medal_type:
            Medal.objects.create(
                type=medal_type,
                olympiad=self.info_olympiad,
                user=self.info_children
            )
