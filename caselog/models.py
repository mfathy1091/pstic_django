from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.dispatch import receiver
from django.db.models.signals import post_save



class PsWorker(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    TEAM = (
        ('NC', 'NC'),
        ('Cairo', 'Cairo'),
    )
    
    NATIONALITY = (
        ('Syria', 'Syria'),
        ('Sudan', 'Sudan'),
        ('S. Sudan', 'S. Sudan'),
        ('Ethiopia', 'Ethiopia'),
        ('Iraq', 'Iraq'),
        ('Somalia', 'Somalia'),
        ('Eritrea', 'Eritrea'),
        ('Yemen', 'Yemen'),
        ('Comoros', 'Comoros'),
        ('Cameron', 'Cameron'),
    )

    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    nationality = models.CharField(max_length=200, null=True, choices=NATIONALITY)
    team = models.CharField(max_length=200, null=True, choices=TEAM)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profilepic = models.ImageField(default='profile_pic.png', null=True, blank=True)

    def __str__(self):
        return self.fullname


class Case(models.Model):
    id = models.AutoField(primary_key=True)
    filenum = models.CharField(max_length=50)
    psworkers = models.ManyToManyField(PsWorker, null=True)

    def __str__(self):
        return self.filenum

class IndirectBenef(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    NATIONALITY = (
        ('Syria', 'Syria'),
        ('Sudan', 'Sudan'),
        ('S. Sudan', 'S. Sudan'),
        ('Ethiopia', 'Ethiopia'),
        ('Iraq', 'Iraq'),
        ('Somalia', 'Somalia'),
        ('Eritrea', 'Eritrea'),
        ('Yemen', 'Yemen'),
        ('Comoros', 'Comoros'),
        ('Cameron', 'Cameron'),
    )

    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    nationality = models.CharField(max_length=200, null=True, choices=NATIONALITY)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fullname


class LogEntry(models.Model):
    MONTH = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        #('May', 'May'),
        #('June', 'June'),
        #('July', 'July'),
        #('August', 'August'),
        #('September', 'September'),
        #('October', 'October'),
        #('November', 'November'),
        #('December', 'December'),
    )
    
    CASETYPE = (
        ('Individual', 'Individual'),
        ('Family', 'Family'),
    )

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    CASESTATUS = (
        ('New', 'New'),
        ('Ongoing', 'Ongoing'),
        ('Inactive', 'Inactive'),
        ('Closed', 'Closed'),
    )
    
    NATIONALITY = (
        ('Syria', 'Syria'),
        ('Sudan', 'Sudan'),
        ('S. Sudan', 'S. Sudan'),
        ('Ethiopia', 'Ethiopia'),
        ('Iraq', 'Iraq'),
        ('Somalia', 'Somalia'),
        ('Eritrea', 'Eritrea'),
        ('Yemen', 'Yemen'),
        ('Comoros', 'Comoros'),
        ('Cameron', 'Cameron'),
    )

    REFERRALSOURCE = (
        ('UNHCR', 'UNHCR'),
        ('Community', 'Community'),
        ('SCI', 'SCI'),
        ('StARS', 'StARS'),
        ('Tdh', 'Tdh'),
        ('PSTIC Hot Line', 'PSTIC Hot Line'),
        ('Egypt Refuge', 'Egypt Refuge'),
        ('IOM', 'IOM'),
    )

    LOCATION = (
        ('Alexandria', 'Alexandria'),
        ('Damietta', 'Damietta'),
        ('Mansoura', 'Mansoura'),
        ('6th of October', '6th of October'),
        ('Ain Shams', 'Ain Shams'),
        ('10th of Ramadan', '10th of Ramadan'),
    )

    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=200, null=True, choices=MONTH)
    filenumber =  models.CharField(max_length=50)
    casestatus = models.CharField(max_length=200, null=True, choices=CASESTATUS)
    casetype = models.CharField(max_length=200, null=True, choices=CASETYPE)
    fullname = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    nationality = models.CharField(max_length=200, null=True, choices=NATIONALITY)
    phone = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True, choices=LOCATION)
    referralsource = models.CharField(max_length=200, null=True, choices=REFERRALSOURCE)
    psworker = models.ForeignKey(PsWorker, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.filenumber
