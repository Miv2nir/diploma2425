# Generated by Django 5.1.6 on 2025-04-09 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_projecttag_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='access',
            field=models.CharField(choices=[('A', 'Public'), ('B', 'Unlisted'), ('C', 'Private')], default='C', max_length=1),
        ),
    ]
