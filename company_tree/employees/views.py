from django.shortcuts import render
from .models import Department

def department_tree_view(request):
    departments = Department.objects.filter(parent=None).prefetch_related('children', 'employees')
    return render(request, 'employees/department_tree.html', {'departments': departments})
