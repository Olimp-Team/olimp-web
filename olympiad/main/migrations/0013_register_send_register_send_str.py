# Generated by Django 5.0.2 on 2024-04-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_register_send_register_send_str_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_send',
            name='Register_send_str',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
