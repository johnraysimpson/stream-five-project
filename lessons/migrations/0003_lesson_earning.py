# Generated by Django 2.0.7 on 2019-10-24 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_lesson_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='earning',
            field=models.DecimalField(decimal_places=2, default=30.0, max_digits=5),
            preserve_default=False,
        ),
    ]
