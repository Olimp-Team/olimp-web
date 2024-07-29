# Generated by Django 5.0.6 on 2024-07-28 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_categories_category_and_more'),
        ('register', '0002_initial'),
        ('school', '0002_alter_school_options_alter_school_address_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='register_send',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='register_send',
            name='Olympiad_send',
        ),
        migrations.RemoveField(
            model_name='register_send',
            name='child_send',
        ),
        migrations.RemoveField(
            model_name='register_send',
            name='school',
        ),
        migrations.RemoveField(
            model_name='register_send',
            name='teacher_send',
        ),
        migrations.RenameField(
            model_name='recommendation',
            old_name='Olympiad',
            new_name='olympiad',
        ),
        migrations.RenameField(
            model_name='register',
            old_name='Olympiad',
            new_name='olympiad',
        ),
        migrations.AlterUniqueTogether(
            name='recommendation',
            unique_together={('recommended_by', 'recommended_to', 'child', 'olympiad')},
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='status',
            field=models.CharField(choices=[('pending', 'В ожидании'), ('accepted', 'Принято'), ('declined', 'Отказано учеником')], default='pending', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='register',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено'),
        ),
        migrations.AlterField(
            model_name='register',
            name='status_send',
            field=models.BooleanField(default=False, verbose_name='Статус отправки'),
        ),
        migrations.AlterField(
            model_name='register',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учитель'),
        ),
        migrations.CreateModel(
            name='RegisterAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_admin', models.BooleanField(default=False, verbose_name='Статус администратора')),
                ('status_teacher', models.BooleanField(default=False, verbose_name='Статус учителя')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('child_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_admin', to=settings.AUTH_USER_MODEL)),
                ('olympiad_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='olympiad_admin', to='main.olympiad')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_register_admin', to='school.school', verbose_name='Школа')),
                ('teacher_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учитель администратор')),
            ],
        ),
        migrations.CreateModel(
            name='RegisterSend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_teacher', models.BooleanField(default=False, verbose_name='Статус учителя')),
                ('status_admin', models.BooleanField(default=False, verbose_name='Статус администратора')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('status_send', models.BooleanField(default=False, verbose_name='Статус отправки')),
                ('child_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_send', to=settings.AUTH_USER_MODEL)),
                ('olympiad_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='olympiad_send', to='main.olympiad')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_register_send', to='school.school', verbose_name='Школа')),
                ('teacher_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Учитель отправитель')),
            ],
            options={
                'unique_together': {('teacher_send', 'child_send', 'olympiad_send')},
            },
        ),
        migrations.DeleteModel(
            name='Register_admin',
        ),
        migrations.DeleteModel(
            name='Register_send',
        ),
    ]
