# Generated by Django 3.1.7 on 2021-03-20 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='beneficiary_statuses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('beneficiary_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='case_statuses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('case_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='genders',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='job_titles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='months',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('month', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='nationalities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nationality', models.CharField(default='Syria', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='nationalitiess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nationality', models.CharField(default='Syria', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='workers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('login_email', models.EmailField(max_length=50)),
                ('login_password', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('gender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.genders')),
                ('job_title_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.job_titles')),
            ],
        ),
        migrations.CreateModel(
            name='cases',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_number', models.CharField(max_length=50)),
                ('case_status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.case_statuses')),
                ('month_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.months')),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.workers')),
            ],
        ),
        migrations.CreateModel(
            name='beneficiaries',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('beneficiary_status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.beneficiary_statuses')),
                ('case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.cases')),
                ('gender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case_log.genders')),
            ],
        ),
    ]
