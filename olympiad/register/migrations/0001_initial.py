# Generated by Django 4.2.11 on 2024-07-22 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_send', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Заявка регистрации на олимпиаду',
                'verbose_name_plural': 'Заявки регистрации на олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Register_admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_admin', models.BooleanField(default=False)),
                ('status_teacher', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Register_send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_teacher', models.BooleanField(default=False)),
                ('status_admin', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('status_send', models.BooleanField(default=False)),
                ('Olympiad_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Olympiad_send', to='main.olympiad')),
            ],
        ),
    ]
