# Generated by Django 5.2 on 2025-06-09 04:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_status_color_task_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='data_input',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
