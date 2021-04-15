from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class PSWorkerForm2(forms.ModelForm):
    class Meta:
        model = PsWorker
        fields = '__all__'
        exclude = ['user']



class MonthForm(forms.Form):
    month = forms.CharField(max_length=100)


class AddCaseForm(forms.Form):
    filenumber = forms.CharField(max_length=100)
    casetype = forms.CharField(max_length=100)
    fullname = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.CharField(max_length=100)
    nationality = forms.CharField(max_length=100)
    month = forms.CharField(max_length=100)

class AddLogEntryForm(forms.Form):
    # month = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : ' dropdown-toggle'}))
    month = forms.CharField(max_length=100)
    casestatus = forms.CharField(max_length=100)
    filenumber = forms.CharField(max_length=100)
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


class LogEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = [
            'month',
            'casestatus',
            'filenumber',
            'casetype',
            'fullname',
            'age',
            'gender',
            'nationality',
            'phone',
            'location',
            'referralsource',
            'psworker', 
        ]



""" class VisitForm(forms.Form):
    visitdate = forms.CharField(max_length=100)
    comment = forms.CharField(
                    widget=forms.Textarea(
                        attrs={'class': 'form-control'}
                    )
    )
    logentry = forms.CharField(
                    widget=forms.TextInput(
                        attrs={'class': 'form-control'}
                        )
    ) """



class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit

        fields = [
            'visitdate',
            'comment',
            'logentry',
        ]

        widgets = {
            'visitdate': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
            'logentry': forms.TextInput(attrs={'class': 'form-control'}),

            #Textarea
            #'placeholder': 'Select Option'
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
 

    
