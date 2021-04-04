from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save



class CaseStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Month(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
	    return self.name


class Gender(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CaseType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PsWorker(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname


class Case(models.Model):
    id = models.AutoField(primary_key=True)
    filenum = models.CharField(max_length=50)
    psworkers = models.ManyToManyField(PsWorker, null=True)

    def __str__(self):
        return self.filenum

class IndirectBenef(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fullname


class LogEntry(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    casestatus = models.ForeignKey(CaseStatus, on_delete=models.CASCADE)
    casetype = models.ForeignKey(CaseType, on_delete=models.CASCADE)
    dfullname = models.CharField(max_length=50)
    dage = models.IntegerField(null=True)
    dgender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    dnationality = models.ForeignKey(Nationality, on_delete=models.CASCADE, null=True)