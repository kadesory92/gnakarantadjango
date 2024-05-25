from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import EmployeeForm
from .forms import ServiceForm, EmployeeAssignmentForm
from django.contrib import messages

from .models import Service, Employee


def manage_service(request):
    services = Service.objects.all()

    # Filtering
    query = request.GET.get('q')
    if query:
        services = services.filter(name__icontains=query)

    # Pagination
    paginator = Paginator(services, 10)  # Show 10 services per page
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        services = paginator.page(1)
    except EmptyPage:
        # If the page is out of bounds (for example, 9999), display the last results page
        services = paginator.page(paginator.num_pages)

    return render(request, 'admin/service/manage_service.html', {'services': services, 'query': query})


def create_service(request):
    if request.method == 'POST':
        service_form = ServiceForm(request.POST)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('admin-dashboard')
    else:
        service_form = ServiceForm()
    return render(request, 'admin/service/create_service.html', {'service_form': service_form})


def service_list(request):
    services = Service.objects.all()

    # Filtering
    query = request.GET.get('q')
    if query:
        services = services.filter(name__icontains=query)

    # Pagination
    paginator = Paginator(services, 10)  # Show 10 services per page
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        services = paginator.page(1)
    except EmptyPage:
        # If the page is out of bounds (for example, 9999), display the last results page
        services = paginator.page(paginator.num_pages)

    return render(request, 'service/service_list.html', {'services': services, 'query': query})


def service_detail(request, id):
    service = get_object_or_404(Service, pk=id)
    employees = Employee.objects.filter(service=service)
    return render(request, 'admin/service/service_detail.html', {'service': service, 'employees': employees})


def detail_service(request, id):
    service = get_object_or_404(Service, pk=id)
    return render(request, 'admin/service/detail_service.html', {'service': service})


def edit_service(request, id):
    service = get_object_or_404(Service, pk=id)

    if request.method == 'POST':
        service_form = ServiceForm(request.POST, instance=service)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('admin.manage_service')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        service_form = ServiceForm(instance=service)
    return render(request, 'admin/service/edit_service.html', {'service_form': service_form})


def delete_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('service_list')
    return render(request, 'service/delete_service_confirm.html', {'service': service})


# In your file views.py

def service_employees(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    employees = Employee.objects.filter(service=service)
    return render(request, 'service/service_employees.html', {'service': service, 'employees': employees})


def manage_employee(request):
    employees = Employee.objects.all()

    # Filtering
    query = request.GET.get('q')
    if query:
        employees = employees.filter(lastname__icontains=query) | \
                    employees.filter(firstname__icontains=query) | \
                    employees.filter(phone__icontains=query) | \
                    employees.filter(position__icontains=query)

    # Pagination
    paginator = Paginator(employees, 10)  # Show 10 services per page
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        employees = paginator.page(1)
    except EmptyPage:
        # If the page is out of bounds (for example, 9999), display the last results page
        employees = paginator.page(paginator.num_pages)
    return render(request, 'admin/employee/manage_employee.html', {'employees': employees, 'query': query})


def employee_list(request):
    employees = Employee.objects.all()

    # Filtering
    query = request.GET.get('q')
    if query:
        employees = employees.filter(firstname__icontains=query) | \
                    employees.filter(lastname__icontains=query) | \
                    employees.filter(position__icontains=query)

    # Pagination
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        employees = paginator.page(1)
    except EmptyPage:
        # If the page is out of bounds (for example, 9999), display the last results page
        employees = paginator.page(paginator.num_pages)

    return render(request, 'employee/employee_list.html', {'employees': employees, 'query': query})


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'employee/employee_detail.html', {'employee': employee})


def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('service_detail', service_id=employee.service.id)
    else:
        employee_form = EmployeeForm(instance=employee)
    return render(request, 'service/update_employee.html', {'employee_form': employee_form, 'employee': employee})


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        service_id = employee.service.id
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('service_detail', service_id=service_id)
    return render(request, 'service/delete_employee_confirm.html', {'employee': employee})


def employee_service(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    service = employee.service
    return render(request, 'employee/employee_service.html', {'employee': employee, 'service': service})


def assign_employee_to_service(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        form = EmployeeAssignmentForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee assigned to service successfully!')
            return redirect('employee_detail', employee_id=employee_id)
    else:
        form = EmployeeAssignmentForm(instance=employee)

    return render(request, 'employee/assign_to_service.html', {'form': form, 'employee': employee})
