# Generated by Django 5.0 on 2024-03-03 08:00

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='Цифра')),
                ('letter', models.CharField(blank=True, max_length=1, null=True, verbose_name='Буква')),
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
            name='Olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название олимпиады')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание олимпиады')),
                ('class_olympiad', models.IntegerField(verbose_name='Класс олимпиады')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
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
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Заявка регистрации на олимпиаду',
                'verbose_name_plural': 'Заявки регистрации на олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Register_send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(verbose_name='Количество намбранных очков')),
                ('status_result',
                 models.CharField(choices=[('У', 'Участник'), ('ПР', 'Призер'), ('ПОБД', 'Победитель')], default='У',
                                  max_length=256, verbose_name='Статус результата')),
            ],
            options={
                'verbose_name': 'Результат олимпиады',
                'verbose_name_plural': 'Резльтаты олимпиад',
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
            name='Сategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория олимпиад',
                'verbose_name_plural': 'Категории олимпиад',
            },
        ),
    ]
