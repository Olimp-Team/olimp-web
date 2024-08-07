# Generated by Django 4.2.11 on 2024-08-07 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Бронзовая лига', 'Бронзовая лига (0-150 очков)'), ('Серебряная лига', 'Серебряная лига (151-500 очков)'), ('Золотая лига', 'Золотая лига (501-1000 очков)'), ('Платиновая лига', 'Платиновая лига (1001-2000 очков)'), ('Рубиновая лига', 'Рубиновая лига (2001-3500 очков)'), ('Алмазная лига', 'Алмазная лига (3501+ очков)'), ('ТОП-250', 'ТОП-250')], max_length=20, verbose_name='Тип лиги')),
                ('min_points', models.IntegerField(verbose_name='Минимальные очки')),
                ('max_points', models.IntegerField(blank=True, null=True, verbose_name='Максимальные очки')),
            ],
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Бронзовая', 'Бронзовая'), ('Серебряная', 'Серебряная'), ('Золотая', 'Золотая'), ('Платиновая', 'Платиновая'), ('Алмазная', 'Алмазная'), ('Рубиновая', 'Рубиновая'), ('Именная', 'Именная')], max_length=20, verbose_name='Тип медали')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalMedal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название медали')),
                ('date_awarded', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0, verbose_name='Очки')),
                ('league', models.CharField(blank=True, choices=[('Бронзовая лига', 'Бронзовая лига (0-150 очков)'), ('Серебряная лига', 'Серебряная лига (151-500 очков)'), ('Золотая лига', 'Золотая лига (501-1000 очков)'), ('Платиновая лига', 'Платиновая лига (1001-2000 очков)'), ('Рубиновая лига', 'Рубиновая лига (2001-3500 очков)'), ('Алмазная лига', 'Алмазная лига (3501+ очков)'), ('ТОП-250', 'ТОП-250')], max_length=20, null=True, verbose_name='Лига')),
            ],
        ),
    ]
