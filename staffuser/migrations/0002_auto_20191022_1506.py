# Generated by Django 2.0.7 on 2019-10-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
