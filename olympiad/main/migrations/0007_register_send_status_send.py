# Generated by Django 5.0.6 on 2024-06-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_register_admin_status_teacher_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_send',
            name='status_send',
            field=models.BooleanField(default=False),
        ),
    ]
