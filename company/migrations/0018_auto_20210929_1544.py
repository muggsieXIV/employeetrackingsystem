# Generated by Django 3.1.6 on 2021-09-29 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_companysettings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CompanySettings',
            new_name='CompanySetting',
        ),
    ]
