# Generated by Django 3.1.6 on 2021-08-16 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clocksystem',
            name='time_worked',
            field=models.CharField(default='00:00:00', max_length=255, null=True),
        ),
    ]
