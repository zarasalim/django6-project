from datetime import date

from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Employee


class EmployeeFilter(filters.FilterSet):
    skills = filters.CharFilter(method='filter_skills')
    experience = filters.NumberFilter(method='filter_experience')

    class Meta:
        model = Employee
        fields = ['skills', 'experience']

    def filter_skills(self, queryset, name, value):
        return queryset.filter(skills__icontains=value)

    def filter_experience(self, queryset, name, value):
        if value < 0:
            return queryset.none()

        today = date.today()
        years = int(value)

        cutoff_date = date(
            today.year - years,
            today.month,
            min(
                today.day,
                28 if today.month == 2 else today.day,
            ),
        )

        return queryset.filter(
            hire_date__isnull=False,
            hire_date__lte=cutoff_date,
        )