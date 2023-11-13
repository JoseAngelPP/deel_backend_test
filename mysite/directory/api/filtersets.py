from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

User = get_user_model()


class UsersFilterSet(filters.FilterSet):
    is_manager = filters.BooleanFilter(method="filter_is_manager")
    has_manager = filters.BooleanFilter(method="filter_has_manager")
    strict = True

    class Meta:
        model = User
        fields = [
            "email",
            "is_active",
        ]

    def filter_is_manager(self, queryset, name, value):
        if value:
            return queryset.filter(reports__isnull=False).distinct()
        return queryset.filter(reports__isnull=True).distinct()

    def filter_has_manager(self, queryset, name, value):
        if value:
            return queryset.filter(reports_to__isnull=False).distinct()
        return queryset.filter(reports_to__isnull=True).distinct()
