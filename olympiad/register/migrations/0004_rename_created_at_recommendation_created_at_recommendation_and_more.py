# Generated by Django 4.2.11 on 2024-07-07 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_register_created_at_register_admin_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recommendation',
            old_name='created_at',
            new_name='created_at_recommendation',
        ),
        migrations.RenameField(
            model_name='register_admin',
            old_name='created_at',
            new_name='created_at_admin',
        ),
        migrations.RenameField(
            model_name='register_send',
            old_name='created_at',
            new_name='created_at_send',
        ),
    ]
