
from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Employee


def add_tenure_days(employees):
    today = date.today()

    for employee in employees:
        if employee.hire_date:
            employee.tenure_days = (
                today - employee.hire_date
            ).days
        else:
            employee.tenure_days = None

    return employees


def home(request):
    employees_count = Employee.objects.count()

    employees = Employee.objects.filter(
        hire_date__isnull=False
    ).order_by('-hire_date', '-pk')[:4]

    employees = add_tenure_days(employees)

    return render(
        request,
        'home.html',
        {
            'employees_count': employees_count,
            'employees': employees,
        },
    )


def employee_list(request):
    employees = Employee.objects.all().order_by(
        'last_name',
        'first_name',
    )

    paginator = Paginator(employees, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    add_tenure_days(page_obj.object_list)

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': page_obj.object_list,
            'page_obj': page_obj,
        },
    )


def employee_detail(request, pk):
    employee = get_object_or_404(
        Employee.objects.prefetch_related('images'),
        pk=pk,
    )

    if employee.hire_date:
        employee.tenure_days = (
            date.today() - employee.hire_date
        ).days
    else:
        employee.tenure_days = None

    images = employee.images.all()
    first_image = images.first()

    gallery = (
        images.exclude(pk=first_image.pk)
        if first_image
        else images
    )

    return render(
        request,
        'employees/employee_detail.html',
        {
            'employee': employee,
            'first_image': first_image,
            'gallery': gallery,
        },
    )