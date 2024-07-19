# Generated by Django 4.2.11 on 2024-07-10 09:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_olympiad_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('result', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='advanced',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Прошел на следующий этап'),
        ),
        migrations.AlterField(
            model_name='result',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='info_children',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Информация об ученике'),
        ),
        migrations.AlterField(
            model_name='result',
            name='info_olympiad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.olympiad', verbose_name='Информация об олимпиаде'),
        ),
        migrations.AlterField(
            model_name='result',
            name='points',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество намбранных очков'),
        ),
        migrations.AlterField(
            model_name='result',
            name='status_result',
            field=models.CharField(blank=True, choices=[('У', 'Участник'), ('ПР', 'Призер'), ('ПОБД', 'Победитель')], default='У', max_length=256, null=True, verbose_name='Статус результата'),
        ),
    ]