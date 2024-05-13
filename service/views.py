from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404

from account.forms import EmployeeForm
from .forms import ServiceForm, EmployeeAssignmentForm
from django.contrib import messages

from .models import Service, Employee


def create_service(request):
    if request.method == 'POST':
        service_form = ServiceForm(request.POST)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, 'Service created successfully!')
            return redirect('dashboard')  # Rediriger vers la page de tableau de bord après la création du service
    else:
        service_form = ServiceForm()
    return render(request, 'registration/register_service.html', {'service_form': service_form})


def service_list(request):
    services = Service.objects.all()

    # Filtrage
    query = request.GET.get('q')
    if query:
        services = services.filter(name__icontains=query)

    # Pagination
    paginator = Paginator(services, 10)  # Afficher 10 services par page
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, affichez la première page
        services = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (par exemple, 9999), affichez la dernière page de résultats
        services = paginator.page(paginator.num_pages)

    return render(request, 'service/service_list.html', {'services': services, 'query': query})


def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    employees = Employee.objects.filter(service=service)
    return render(request, 'service/service_detail.html', {'service': service, 'employees': employees})


def update_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        service_form = ServiceForm(request.POST, instance=service)
        if service_form.is_valid():
            service_form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('service_list')
    else:
        service_form = ServiceForm(instance=service)
    return render(request, 'service/update_service.html', {'service_form': service_form})


def delete_service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('service_list')
    return render(request, 'service/delete_service_confirm.html', {'service': service})


# Dans votre fichier views.py

def service_employees(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    employees = Employee.objects.filter(service=service)
    return render(request, 'service/service_employees.html', {'service': service, 'employees': employees})


def employee_list(request):
    employees = Employee.objects.all()

    # Filtrage
    query = request.GET.get('q')
    if query:
        employees = employees.filter(firstname__icontains=query) | \
                    employees.filter(lastname__icontains=query) | \
                    employees.filter(position__icontains=query)

    # Pagination
    paginator = Paginator(employees, 10)  # Afficher 10 employés par page
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, affichez la première page
        employees = paginator.page(1)
    except EmptyPage:
        # Si la page est hors limites (par exemple, 9999), affichez la dernière page de résultats
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
