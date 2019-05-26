import django_filters
from django.db import models

from .models import Demand


class DemandFilter(django_filters.FilterSet):
    start_date_gte = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_lte = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')
    end_date_gte = django_filters.DateFilter(field_name='end_date', lookup_expr='gte')
    end_date_lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    frequency_gte = django_filters.NumberFilter(field_name='frequency', lookup_expr='gte')
    frequency_lte = django_filters.NumberFilter(field_name='frequency', lookup_expr='lte')

    class Meta:
        model = Demand
        # exclude = ['comment', 'user_create', 'time_create', 'user_update', 'time_update']
        fields = ['product', 'tech_node', 'content']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


class DemandAnalysisFilter(django_filters.FilterSet):
    start_date_gte = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date_lte = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = Demand
        fields = ['start_date_gte', 'end_date_lte']

