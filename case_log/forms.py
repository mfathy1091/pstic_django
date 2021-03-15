from django import forms

from .models import workers, genders, job_titles, cases, months


class WorkerForm(forms.ModelForm):
    class Meta:
        model = workers
        fields = [
            'first_name',
            'last_name',
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
            'worker_id',
            'case_status_id',
        ]

