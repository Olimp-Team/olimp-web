# Generated by Django 4.2.11 on 2024-07-22 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        ('main', '0002_initial'),
        ('result', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='info_children',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Информация об ученике'),
        ),
        migrations.AddField(
            model_name='result',
            name='info_olympiad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.olympiad', verbose_name='Информация об олимпиаде'),
        ),
        migrations.AddField(
            model_name='result',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_result', to='school.school', verbose_name='Школа'),
        ),
    ]
