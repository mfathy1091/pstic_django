from django import forms

from .models import PsWorker, Gender, Case, Month, Nationality, IndirectBenef, CaseType


class PSWorkerForm(forms.ModelForm):
    class Meta:
        model = PsWorker
        fields = [
            'fullname',
            'age',
            'gender',
            'nationality'
        ]


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'filenum',
        ]




class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = [
            'name',
        ]


class NationalityForm(forms.ModelForm):
    class Meta:
        model = Nationality
        fields = [
            'name',
        ]


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
    

class FilterByMonthForm(forms.Form):
    month = forms.CharField(max_length=100)

