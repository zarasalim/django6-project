
from django.contrib import admin
from .models import Employee, EmployeeImage


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender')
    search_fields = ('first_name', 'last_name')
    inlines = [EmployeeImageInline]


@admin.register(EmployeeImage)
class EmployeeImageAdmin(admin.ModelAdmin):
    list_display = ('employee', 'order')
    ordering = ('employee', 'order')