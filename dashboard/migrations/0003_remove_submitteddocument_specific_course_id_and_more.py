# Generated by Django 5.0.2 on 2024-05-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_submitteddocument_accepted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submitteddocument',
            name='specific_course_id',
        ),
        migrations.AlterField(
            model_name='submitteddocument',
            name='from_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='submitteddocument',
            name='to_date',
            field=models.DateTimeField(),
        ),
    ]