# Generated by Django 3.1.6 on 2021-09-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_auto_20210903_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]