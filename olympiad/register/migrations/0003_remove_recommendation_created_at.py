# Generated by Django 4.2.11 on 2024-07-09 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='created_at',
        ),
    ]
