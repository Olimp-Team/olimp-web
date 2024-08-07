# Generated by Django 4.2.11 on 2024-08-07 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('result', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0001_initial'),
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='info_children',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Информация об ученике'),
        ),
        migrations.AddField(
            model_name='result',
            name='info_olympiad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.olympiad', verbose_name='Информация об олимпиаде'),
        ),
        migrations.AddField(
            model_name='result',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school', verbose_name='Школа'),
        ),
    ]
