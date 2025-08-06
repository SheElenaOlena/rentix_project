import django_filters

from apps.listings.models import Listing


class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    rooms = django_filters.RangeFilter()
    city = django_filters.CharFilter(field_name='location__city', lookup_expr='icontains')
    property_type = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Listing
        fields = []