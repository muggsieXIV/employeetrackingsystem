# Generated by Django 3.1.6 on 2021-09-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_auto_20210903_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(null=True, upload_to='media/logos/'),
        ),
    ]
