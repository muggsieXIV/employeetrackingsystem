# Generated by Django 3.1.6 on 2021-09-30 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0025_auto_20210930_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(null=True, upload_to='company-image'),
        ),
    ]
