# Generated by Django 5.0.2 on 2024-05-15 12:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0018_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specific_course',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 15, 12, 16, 2, 522435, tzinfo=datetime.timezone.utc)),
        ),
    ]