# Generated by Django 5.0.1 on 2024-02-28 03:01


import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('users_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='USER_ADMIN', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Администратор',
                'verbose_name_plural': 'Администраторы',
            },
            bases=('users.users',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('users_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='USER_CHILD', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.classroom', verbose_name='Класс ученика')),
            ],
            options={
                'verbose_name': 'Ученик',
                'verbose_name_plural': 'Ученики',
            },
            bases=('users.users',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название олимпиады')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание олимпиады')),
                ('class_olympiad', models.IntegerField(verbose_name='Класс олимпиады')),
                ('date_olympiad', models.DateTimeField(verbose_name='Дата проведения олимпиады')),
                ('level', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='main.level_olympiad', verbose_name='Название уровня')),
                ('stage', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='main.stage', verbose_name='Название этапа')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject', verbose_name='Название школьного предмета')),
                ('category', models.ForeignKey(max_length=256, on_delete=django.db.models.deletion.CASCADE, to='main.сategory', verbose_name='Категория олимпиады')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('Olympiad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.olympiad')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заявка регистрации на олимпиаду',
                'verbose_name_plural': 'Заявки регистрации на олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(verbose_name='Количество намбранных очков')),
                ('status_result', models.CharField(choices=[('У', 'Участник'), ('ПР', 'Призер'), ('ПОБД', 'Победитель')], default='У', max_length=256, verbose_name='Статус результата')),
                ('info_children', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.child', verbose_name='Информация об ученике')),
                ('info_olympiad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.olympiad', verbose_name='Информация об олимпиаде')),
            ],
            options={
                'verbose_name': 'Результат олимпиады',
                'verbose_name_plural': 'Резльтаты олимпиад',
            },
        ),
        migrations.CreateModel(
            name='History_result_olympiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_results', models.DateTimeField()),
                ('info_results', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.result', verbose_name='Информация о результате')),
            ],
            options={
                'verbose_name': 'Истрия результата олимпиады',
                'verbose_name_plural': 'История результатов олимпиад',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('users_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classroom_guide', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.classroom', verbose_name='Классное руководство')),
                ('post_job_teacher', models.ManyToManyField(to='main.post', verbose_name='Должность учителя')),
                ('subject', models.ManyToManyField(blank=True, to='main.subject', verbose_name='Какой предмет ведёт учитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='USER_TEACHER', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Учитель',
                'verbose_name_plural': 'Учителя',
            },
            bases=('users.users',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='classroom',
            name='info_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='info_teacher', to='main.teacher'),
        ),
    ]
