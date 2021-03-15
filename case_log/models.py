from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class genders(models.Model):
    id = models.AutoField(primary_key=True)
    gender_type = models.CharField(max_length=50)

    def __str__(self):
        return self.gender_type

class job_titles(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=50)

    def __str__(self):
	    return self.job_title


class workers(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    login_email = models.EmailField(max_length=50)
    login_password = models.CharField(max_length=50)
    age = models.IntegerField()
    gender_id = models.ForeignKey(genders, on_delete=models.CASCADE)
    job_title_id = models.ForeignKey(job_titles, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class months(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=50)

    def __str__(self):
	    return self.month

    


    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

class case_statuses(models.Model):
    id = models.AutoField(primary_key=True)
    case_status = models.CharField(max_length=50)

    def __str__(self):
	    return self.case_status


class cases(models.Model):
    id = models.AutoField(primary_key=True)
    month_id = models.ForeignKey(months, on_delete=models.CASCADE)
    file_number = models.CharField(max_length=50)
    worker_id = models.ForeignKey(workers, on_delete=models.CASCADE)
    case_status_id = models.ForeignKey(case_statuses, on_delete=models.CASCADE)
    


class beneficiary_statuses(models.Model):
    id = models.AutoField(primary_key=True)
    beneficiary_status = models.CharField(max_length=50)

    def __str__(self):
	    return self.beneficiary_status

class beneficiaries(models.Model):
    id = models.AutoField(primary_key=True)
    file_number_id = models.ForeignKey(cases, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender_id = models.ForeignKey(genders, on_delete=models.CASCADE)
    beneficiary_status_id = models.ForeignKey(beneficiary_statuses, on_delete=models.CASCADE)

    def __str__(self):
	    return self.full_name