# Generated by Django 5.1.6 on 2025-05-05 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_functionstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='functionstatus',
            name='info',
            field=models.JSONField(blank=True, default={}),
        ),
    ]
