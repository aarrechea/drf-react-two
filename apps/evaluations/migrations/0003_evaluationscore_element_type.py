# Generated by Django 5.0.2 on 2024-11-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_evaluations', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationscore',
            name='element_type',
            field=models.IntegerField(default=0),
        ),
    ]