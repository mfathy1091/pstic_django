from django import forms

from .models import workers, genders, job_titles


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
