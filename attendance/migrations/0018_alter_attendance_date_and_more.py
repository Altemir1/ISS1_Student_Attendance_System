# Generated by Django 4.2.3 on 2024-05-07 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0017_alter_specific_course_registration_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='specific_course',
            name='registration_deadline',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 7, 17, 42, 44, 356789, tzinfo=datetime.timezone.utc)),
        ),
    ]