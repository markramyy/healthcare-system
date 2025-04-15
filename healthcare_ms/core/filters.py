import django_filters

from datetime import timedelta
from django.utils import timezone

from healthcare_ms.core.models import DBBase


class BaseFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='is_active')
    time_range = django_filters.CharFilter(method='filter_time_range')

    def filter_time_range(self, queryset, name, value):
        if value == 'past_hour':
            return queryset.filter(created__gte=timezone.now() - timedelta(hours=1))
        elif value == 'past_24_hours':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=1))
        elif value == 'past_week':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=7))
        elif value == 'past_month':
            return queryset.filter(created__gte=timezone.now() - timedelta(days=30))
        elif value.startswith('custom_range:'):
            date_range = value.split('custom_range:')[1].split('to')
            start_date = date_range[0].strip()
            end_date = date_range[1].strip()
            return queryset.filter(created__date__gte=start_date, created__date__lte=end_date)
        return queryset

    class Meta:
        model = DBBase  # Replace DBBase with your specific model if needed
        fields = ['is_active', 'time_range']
