# Generated by Django 4.2.3 on 2024-03-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_rename_manually_recorded_attendance_present_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='is_lecture',
            field=models.BooleanField(default=False),
        ),
    ]