# Generated by Django 4.2.3 on 2024-05-15 19:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0021_alter_specific_course_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specific_course',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 15, 19, 49, 6, 598442, tzinfo=datetime.timezone.utc)),
        ),
    ]
