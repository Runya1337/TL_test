from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Department, Employee

admin.site.register(Department, MPTTModelAdmin)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'hire_date', 'salary', 'department']

