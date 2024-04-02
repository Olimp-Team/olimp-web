# Generated by Django 5.0.2 on 2024-04-02 18:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_register_send_register_send_str'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='register_admin',
            name='Olympiad_admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Olympiad_admin', to='main.olympiad'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register_admin',
            name='child_admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='child_admin', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register_admin',
            name='teacher_admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='teacher_admin'),
            preserve_default=False,
        ),
    ]
