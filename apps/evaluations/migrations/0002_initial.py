# Generated by Django 5.0.2 on 2024-11-08 22:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apps_evaluations', '0001_initial'),
        ('apps_relations_tree', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationscore',
            name='relation_tree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relation_tree_related', to='apps_relations_tree.relationtree'),
        ),
        migrations.AddField(
            model_name='mainproducts',
            name='evaluation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps_evaluations.evaluation'),
        ),
    ]
