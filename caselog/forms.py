from django import forms

from .models import *


class PSWorkerForm(forms.ModelForm):
    class Meta:
        model = PsWorker
        fields = [
            'fullname',
            'phone',
            'email',
            'age',
            'gender',
            'nationality',
            'team',
        ]


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'filenum',
        ]


class MonthForm(forms.Form):
    month = forms.CharField(max_length=100)


class AddCaseForm(forms.Form):
    filenum = forms.CharField(max_length=100)
    casetype = forms.CharField(max_length=100)
    fullname = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.CharField(max_length=100)
    nationality = forms.CharField(max_length=100)
    month = forms.CharField(max_length=100)

class AddLogEntryForm(forms.Form):
    month = forms.CharField(max_length=100)
    casestatus = forms.CharField(max_length=100)
    filenum = forms.CharField(max_length=100)
    casetype = forms.CharField(max_length=100)
    fullname = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.CharField(max_length=100)
    nationality = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    referralsource = forms.CharField(max_length=100)
    psworker = forms.CharField(max_length=100)
    

class FilterByMonthForm(forms.Form):
    month = forms.CharField(max_length=100)

