# Generated by Django 5.1.4 on 2025-01-09 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_task_is_overdue_alter_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
