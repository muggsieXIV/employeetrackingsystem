# Generated by Django 3.1.6 on 2021-09-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0015_auto_20210928_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
