# Generated by Django 5.0.2 on 2024-04-02 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_register_admin_register_admin_str'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_admin',
            name='Register_admin_str',
            field=models.TextField(blank=True, null=True),
        ),
    ]
