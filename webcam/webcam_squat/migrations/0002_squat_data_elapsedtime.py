# Generated by Django 5.0.6 on 2024-06-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcam_squat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='squat_data',
            name='elapsedtime',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
