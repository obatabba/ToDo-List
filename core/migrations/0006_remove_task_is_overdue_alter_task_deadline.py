# Generated by Django 5.1.4 on 2025-01-07 23:11

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_task_is_overdue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_overdue',
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=core.models.default_deadline),
        ),
    ]
