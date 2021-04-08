# Generated by Django 3.1.7 on 2021-04-08 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caselog', '0010_auto_20210403_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='dage',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='dfullname',
            new_name='fullname',
        ),
        migrations.RemoveField(
            model_name='logentry',
            name='dgender',
        ),
        migrations.RemoveField(
            model_name='logentry',
            name='dnationality',
        ),
        migrations.AddField(
            model_name='logentry',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='logentry',
            name='nationality',
            field=models.CharField(choices=[('Syria', 'Syria'), ('Sudan', 'Sudan'), ('S. Sudan', 'S. Sudan'), ('Ethiopia', 'Ethiopia'), ('Iraq', 'Iraq'), ('Somalia', 'Somalia'), ('Eritrea', 'Eritrea'), ('Yemen', 'Yemen'), ('Comoros', 'Comoros'), ('Cameron', 'Cameron')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='indirectbenef',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='indirectbenef',
            name='nationality',
            field=models.CharField(choices=[('Syria', 'Syria'), ('Sudan', 'Sudan'), ('S. Sudan', 'S. Sudan'), ('Ethiopia', 'Ethiopia'), ('Iraq', 'Iraq'), ('Somalia', 'Somalia'), ('Eritrea', 'Eritrea'), ('Yemen', 'Yemen'), ('Comoros', 'Comoros'), ('Cameron', 'Cameron')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='casestatus',
            field=models.CharField(choices=[('New', 'New'), ('Ongoing', 'Ongoing'), ('Inactive', 'Inactive'), ('Closed', 'Closed')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='casetype',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Family', 'Family')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='month',
            field=models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='psworker',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='psworker',
            name='nationality',
            field=models.CharField(choices=[('Syria', 'Syria'), ('Sudan', 'Sudan'), ('S. Sudan', 'S. Sudan'), ('Ethiopia', 'Ethiopia'), ('Iraq', 'Iraq'), ('Somalia', 'Somalia'), ('Eritrea', 'Eritrea'), ('Yemen', 'Yemen'), ('Comoros', 'Comoros'), ('Cameron', 'Cameron')], max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='CaseStatus',
        ),
        migrations.DeleteModel(
            name='CaseType',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
        migrations.DeleteModel(
            name='Month',
        ),
        migrations.DeleteModel(
            name='Nationality',
        ),
    ]