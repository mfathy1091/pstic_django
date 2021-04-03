from django.contrib import admin
from .models import PsWorker, Case, DirectBenef, IndirectBenef

admin.site.register(PsWorker)
admin.site.register(Case)
admin.site.register(DirectBenef)
admin.site.register(IndirectBenef)