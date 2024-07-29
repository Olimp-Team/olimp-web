from django.db import models
from users.models import User
from main.models import Olympiad
from school.models import School


class League(models.Model):
    """Модель лиги с диапазоном очков и типами лиг"""
    BRONZE = 'Бронзовая лига'
    SILVER = 'Серебряная лига'
    GOLD = 'Золотая лига'
    PLATINUM = 'Платиновая лига'
    RUBY = 'Рубиновая лига'
    DIAMOND = 'Алмазная лига'
    TOP_250 = 'ТОП-250'

    LEAGUE_TYPES = [
        (BRONZE, 'Бронзовая лига (0-150 очков)'),
        (SILVER, 'Серебряная лига (151-500 очков)'),
        (GOLD, 'Золотая лига (501-1000 очков)'),
        (PLATINUM, 'Платиновая лига (1001-2000 очков)'),
        (RUBY, 'Рубиновая лига (2001-3500 очков)'),
        (DIAMOND, 'Алмазная лига (3501+ очков)'),
        (TOP_250, 'ТОП-250'),
    ]

    type = models.CharField('Тип лиги', max_length=20, choices=LEAGUE_TYPES)
    min_points = models.IntegerField('Минимальные очки')
    max_points = models.IntegerField('Максимальные очки', blank=True, null=True)

    def __str__(self):
        return self.get_type_display()

    @staticmethod
    def get_league_for_points(points):
        """Возвращает тип лиги в зависимости от количества очков"""
        if points <= 150:
            return League.BRONZE
        elif points <= 500:
            return League.SILVER
        elif points <= 1000:
            return League.GOLD
        elif points <= 2000:
            return League.PLATINUM
        elif points <= 3500:
            return League.RUBY
        elif points > 3500:
            return League.DIAMOND


class Medal(models.Model):
    """Модель медали, связанная с пользователем и олимпиадой"""
    BRONZE = 'Бронзовая'
    SILVER = 'Серебряная'
    GOLD = 'Золотая'
    PLATINUM = 'Платиновая'
    DIAMOND = 'Алмазная'
    RUBY = 'Рубиновая'
    PERSONAL = 'Именная'

    MEDAL_TYPES = [
        (BRONZE, 'Бронзовая'),
        (SILVER, 'Серебряная'),
        (GOLD, 'Золотая'),
        (PLATINUM, 'Платиновая'),
        (DIAMOND, 'Алмазная'),
        (RUBY, 'Рубиновая'),
        (PERSONAL, 'Именная'),
    ]

    type = models.CharField('Тип медали', max_length=20, choices=MEDAL_TYPES)
    olympiad = models.ForeignKey('main.Olympiad', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type} - {self.olympiad} - {self.user}'


class Rating(models.Model):
    """Модель рейтинга пользователя с очками и лигой"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    points = models.IntegerField('Очки', default=0)
    league = models.CharField('Лига', max_length=20, choices=League.LEAGUE_TYPES, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.points} очков - {self.league}'

    def update_points(self, additional_points):
        """Обновляет очки пользователя и пересчитывает его лигу"""
        self.points += additional_points
        self.league = League.get_league_for_points(self.points)
        self.save()


class PersonalMedal(models.Model):
    """Модель именной медали, связанная с пользователем"""
    name = models.CharField('Название медали', max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_awarded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.user}'
