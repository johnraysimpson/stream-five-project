# Generated by Django 2.0.7 on 2019-10-15 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staffuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
