# Generated by Django 3.1.6 on 2021-08-17 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ('id', 'last_name', 'first_name', 'is_active', 'role', 'company')},
        ),
    ]
