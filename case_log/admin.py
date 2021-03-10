from django.contrib import admin

from .models import workers, job_titles

admin.site.register(workers)

admin.site.register(job_titles)
