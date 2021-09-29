# Generated by Django 3.1.6 on 2021-09-29 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0020_auto_20210929_1600'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companysetting',
            options={'ordering': ('id', 'company', 'color', 'font_color', 'background_color', 'time_zone', 'created_at', 'updated_at')},
        ),
        migrations.AddField(
            model_name='companysetting',
            name='time_zone',
            field=models.CharField(default="USTimeZone(-6, 'Central',  'CST', 'CDT')", max_length=200, null=True),
        ),
    ]