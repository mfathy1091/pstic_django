from django import forms

from .models import workers, genders, job_titles, cases, beneficiaries, months, nationalities


class WorkerForm(forms.ModelForm):
    class Meta:
        model = workers
        fields = [
            'fname',
            'lname',
            'login_email',
            'login_password',
            'age',
            'gender_id',
            'job_title_id'
        ]


class CaseForm(forms.ModelForm):
    class Meta:
        model = cases
        fields = [
            'file_number',
            'month_id',
            'nationality_id',
            'worker_id',
            'case_status_id',
        ]


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = beneficiaries
        fields = [
            'case_id',
            'full_name',
            'age',
            'gender_id',
            'beneficiary_status_id',
        ]


