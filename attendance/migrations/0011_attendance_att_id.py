# Generated by Django 5.0.2 on 2024-04-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_specific_course_is_lecture'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='att_id',
            field=models.IntegerField(default=0),
        ),
    ]