# Generated by Django 4.2.11 on 2024-07-24 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
        ('main', '0004_alter_olympiad_school'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='olympiad',
            options={},
        ),
        migrations.RemoveField(
            model_name='olympiad',
            name='time',
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categories'),
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='class_olympiad',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.level_olympiad'),
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='location',
            field=models.CharField(blank=True, default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.school'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.stage'),
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.subject'),
        ),
    ]
