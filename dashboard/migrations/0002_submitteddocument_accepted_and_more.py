# Generated by Django 4.2.3 on 2024-05-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitteddocument',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submitteddocument',
            name='from_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='submitteddocument',
            name='specific_course_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='submitteddocument',
            name='to_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]