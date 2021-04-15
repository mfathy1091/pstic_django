import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class LogEntryFilter(django_filters.FilterSet):
    #start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    #End_date = DateFilter(field_name="date_created", lookup_expr='lte')
    #note = CharFilter(field_name="note", lookup_expr='icontains')
    class Meta:
        model = LogEntry
        #fields = '__all__'
        fields = ['month', 'filenumber', 'casestatus']
        #exclude = ['psworker', 'age', 'location', 'phone']
