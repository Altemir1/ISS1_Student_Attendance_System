# Generated by Django 5.0.2 on 2024-04-24 02:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_alter_attendance_att_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='specific_course',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 24, 2, 29, 1, 942490, tzinfo=datetime.timezone.utc)),
        ),
    ]