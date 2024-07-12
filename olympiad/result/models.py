from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
                                      verbose_name='Информация об ученике', blank=True, null=True)
    info_olympiad = models.ForeignKey(to='main.Olympiad', on_delete=models.CASCADE,
                                      verbose_name='Информация об олимпиаде', blank=True, null=True)
    points = models.IntegerField(verbose_name='Количество намбранных очков', blank=True, null=True)
    status_result = models.CharField(verbose_name='Статус результата', max_length=256, choices=STATUSRES,
                                     default=PARTICIPANT, blank=True, null=True)
    advanced = models.BooleanField(default=False, verbose_name='Прошел на следующий этап', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.info_children} - {self.info_olympiad} - {self.points}'
