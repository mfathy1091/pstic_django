# Generated by Django 3.1.7 on 2021-04-10 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caselog', '0014_auto_20210409_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='psworker',
            name='team',
            field=models.CharField(choices=[('NC', 'NC'), ('Cairo', 'Cairo')], max_length=200, null=True),
        ),
    ]
