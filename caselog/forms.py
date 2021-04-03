from django import forms

from .models import PsWorker, Gender, Case, Month, Nationality, DirectBenef, IndirectBenef, CaseType


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


class IndirectBenefForm(forms.ModelForm):
    class Meta:
        model = DirectBenef
        fields = [
            'fullname',
            'age',
            'gender',
            'nationality',
        ]


class DirectBenefForm(forms.ModelForm):
    class Meta:
        model = IndirectBenef
        fields = [
            'fullname',
            'age',
            'gender',
            'nationality',
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
    

#class CaseForm2(forms.Form):
#    post = forms.CharField()

