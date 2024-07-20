# Generated by Django 4.2.11 on 2024-07-20 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=256, verbose_name='Действие')),
                ('object_name', models.CharField(max_length=256, verbose_name='Объект')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время действия')),
            ],
        ),
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория олимпиад',
                'verbose_name_plural': 'Категории олимпиад',
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Цифра')),
                ('letter', models.CharField(blank=True, max_length=1, null=True, verbose_name='Буква')),
                ('is_graduated', models.BooleanField(default=False, verbose_name='Выпустился')),
                ('graduation_year', models.IntegerField(blank=True, null=True, verbose_name='Год выпуска')),
            ],
            options={
                'verbose_name': 'Учебный класс',
                'verbose_name_plural': 'Учебные классы',
            },
        ),
        migrations.CreateModel(
            name='Level_olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название уровня')),
            ],
            options={
                'verbose_name': 'Уровень олимпиад',
                'verbose_name_plural': 'Уровень олимпиад',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Этап олимпиады',
                'verbose_name_plural': 'Этапы олимпиад',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название школьного предмета')),
            ],
            options={
                'verbose_name': 'Школьный предмет',
                'verbose_name_plural': 'Школьные предметы',
            },
        ),
        migrations.CreateModel(
            name='Olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название олимпиады')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание олимпиады')),
                ('class_olympiad', models.IntegerField(verbose_name='Класс олимпиады')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата проведения')),
                ('location', models.CharField(blank=True, max_length=256, null=True, verbose_name='Место проведения олимпиады')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categories', verbose_name='Категория олимпиады')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.level_olympiad', verbose_name='Название уровня')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.stage', verbose_name='Название этапа')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject', verbose_name='Название школьного предмета')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
            },
        ),
    ]
