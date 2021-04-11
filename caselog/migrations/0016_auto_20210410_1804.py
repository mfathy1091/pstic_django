# Generated by Django 3.1.7 on 2021-04-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caselog', '0015_psworker_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logentry',
            name='case',
        ),
        migrations.AddField(
            model_name='logentry',
            name='filenumber',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]