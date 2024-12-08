import django_filters
from django_filters import DateFilter

from .models import *

class AssignmentFilter(django_filters.FilterSet):
    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ['description', 'date_created']