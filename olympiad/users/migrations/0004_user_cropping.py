# Generated by Django 4.2.11 on 2024-07-20 12:53

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_cropping'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
    ]
