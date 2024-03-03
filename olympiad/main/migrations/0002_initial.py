# Generated by Django 5.0 on 2024-03-03 08:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='child',
            field=models.ManyToManyField(blank=True, related_name='Child', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='olympiad',
            name='level',
            field=models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='main.level_olympiad', verbose_name='Название уровня'),
        ),
        migrations.AddField(
            model_name='register',
            name='Olympiad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.olympiad'),
        ),
        migrations.AddField(
            model_name='register',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ученик', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='register',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=''),
        ),
        migrations.AddField(
            model_name='register_send',
            name='Register',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Register', to='main.register'),
        ),
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
            model_name='olympiad',
            name='stage',
            field=models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='main.stage', verbose_name='Название этапа'),
        ),
        migrations.AddField(
            model_name='olympiad',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject', verbose_name='Название школьного предмета'),
        ),
        migrations.AddField(
            model_name='olympiad',
            name='category',
            field=models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='main.сategory', verbose_name='Категория олимпиады'),
        ),
    ]
