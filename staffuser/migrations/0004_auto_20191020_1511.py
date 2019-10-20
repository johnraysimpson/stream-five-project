# Generated by Django 2.0.7 on 2019-10-20 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffuser', '0003_student_price_per_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentsession',
            name='sessions',
        ),
        migrations.RemoveField(
            model_name='studentsession',
            name='student',
        ),
        migrations.RemoveField(
            model_name='tutorsession',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='StudentSession',
        ),
        migrations.DeleteModel(
            name='TutorSession',
        ),
    ]
