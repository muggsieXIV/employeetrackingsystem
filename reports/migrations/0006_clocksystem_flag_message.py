# Generated by Django 3.1.6 on 2021-09-29 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_auto_20210906_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='clocksystem',
            name='flag_message',
            field=models.TimeField(null=True),
        ),
    ]
