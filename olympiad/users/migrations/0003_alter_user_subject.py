# Generated by Django 5.0.6 on 2024-07-28 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_categories_category_and_more'),
        ('users', '0002_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subject',
            field=models.ManyToManyField(blank=True, to='main.subject', verbose_name='Какой предмет ведёт учитель'),
        ),
    ]
