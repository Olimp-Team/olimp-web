from django.db import models
from users.models import User


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
    info_olympiad = models.ForeignKey(to='main.Olympiad', on_delete=models.CASCADE,
                                      verbose_name='Информация об олимпиаде')
    points = models.IntegerField(verbose_name='Количество намбранных очков')
    status_result = models.CharField(verbose_name='Статус результата', max_length=256, choices=STATUSRES,
                                     default=PARTICIPANT)
    advanced = models.BooleanField(default=False, verbose_name='Прошел на следующий этап')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.info_children} - {self.info_olympiad} - {self.points}'
