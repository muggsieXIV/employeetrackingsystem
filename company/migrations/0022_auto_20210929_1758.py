# Generated by Django 3.1.6 on 2021-09-29 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_auto_20210929_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysetting',
            name='time_zone',
            field=models.CharField(default='US/Central', max_length=200, null=True),
        ),
    ]
