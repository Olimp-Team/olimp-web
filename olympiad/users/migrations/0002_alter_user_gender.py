# Generated by Django 4.2.11 on 2024-05-15 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('М', 'Male'), ('Ж', 'Womens')], default='М', max_length=2, verbose_name='Пол учителя'),
        ),
    ]