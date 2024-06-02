import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import required_role
from account.forms import EmployeeForm
from core.models import Student
from school.models import School, Staff
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

    return render(request, 'admin/employee/employee_list.html', {'employees': employees, 'query': query})


# def employee_detail(request, id):
#     employee = get_object_or_404(Employee, pk=id)
#     return render(request, 'admin/employee/employee_detail.html', {'employee': employee})


def employee_detail(request, id):
    try:
        employee = get_object_or_404(Employee, pk=id)
        return render(request, 'admin/employee/employee_detail.html', {'employee': employee})
    except Http404:
        messages.error(request, 'Employee not found.')
        return redirect('admin.manage_employee')


def edit_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if employee_form.is_valid():
            employee_form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('admin.manage_employee')
        else:
            messages.error(request, 'There was an error in the form. Please correct the errors below.')
    else:
        employee_form = EmployeeForm(instance=employee)
    return render(request, 'admin/employee/edit_employee.html', {'employee_form': employee_form})


def delete_employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    if request.method == 'POST':
        # service_id = employee.service.id

        # Delete the photo from the storage
        if employee.photo.url:
            photo_path = os.path.join(settings.MEDIA_ROOT, employee.photo.url)
            if os.path.isfile(photo_path):
                os.remove(photo_path)

        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('admin.manage_employee')  # , service_id=service_id

    return render(request, 'admin/employee/delete_employee_confirm.html', {'employee': employee})


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


@login_required(login_url='login')
def service_dashboard(request):
    user = request.user

    # Vérification du rôle de l'utilisateur pour déterminer le service concerné
    if user.role not in ['ADMIN_DPE', 'ADMIN_DCE', 'ADMIN_IRE']:
        raise PermissionDenied

    try:
        # Récupérer l'employé lié à l'utilisateur connecté
        employee = Employee.objects.get(user=user)

        # Déterminer le service concerné en fonction du rôle de l'utilisateur
        if user.role == 'ADMIN_IRE':
            user_service = employee.service
            # Récupérer toutes les écoles sous cette inspection régionale (ire)
            schools = School.objects.filter(ire=user_service)
        else:
            user_service = employee.service
            # Récupérer toutes les écoles sous cette direction
            schools = School.objects.filter(direction=user_service)

        # Récupérer les critères de recherche et de filtrage des paramètres de la requête
        search_query = request.GET.get('search', '')
        filter_by_role = request.GET.get('role', '')

        # Filtrer les étudiants, enseignants et personnels des écoles sous la direction ou l'ire
        students = Student.objects.filter(school__in=schools, user__username__icontains=search_query)
        teachers = Staff.objects.filter(school__in=schools, user__role='TEACHER',
                                        user__username__icontains=search_query)
        staff = Staff.objects.filter(school__in=schools).exclude(user__role='TEACHER').filter(
            user__username__icontains=search_query)

        if filter_by_role:
            students = students.filter(user__role=filter_by_role)
            teachers = teachers.filter(user__role=filter_by_role)
            staff = staff.filter(user__role=filter_by_role)

        # Pagination
        paginator_students = Paginator(students, 10)  # 10 étudiants par page
        paginator_teachers = Paginator(teachers, 10)  # 10 enseignants par page
        paginator_staff = Paginator(staff, 10)  # 10 personnels par page

        page_number_students = request.GET.get('page_students', 1)
        page_number_teachers = request.GET.get('page_teachers', 1)
        page_number_staff = request.GET.get('page_staff', 1)

        students_page = paginator_students.get_page(page_number_students)
        teachers_page = paginator_teachers.get_page(page_number_teachers)
        staff_page = paginator_staff.get_page(page_number_staff)

        context = {
            'schools': schools,
            'students': students_page,
            'teachers': teachers_page,
            'staff': staff_page,
            'search_query': search_query,
            'filter_by_role': filter_by_role,
        }

        return render(request, 'service/admin/dashboard.html', context)

    except Employee.DoesNotExist:
        raise PermissionDenied


# @login_required
# def service_dashboard(request):
#     user = request.user
#
#     # Vérifiez que l'utilisateur est un employé avec le rôle approprié
#     if user.role not in ['ADMIN_DPE', 'ADMIN_DCE']:
#         raise PermissionDenied
#
#     try:
#         # Récupérer l'employé lié à l'utilisateur connecté
#         employee = Employee.objects.get(user=user)
#
#         # Récupérer le service de cet employé
#         user_service = employee.service
#
#         # Récupérer toutes les écoles sous cette direction
#         schools = School.objects.filter(direction=user_service)
#
#         # Récupérer tous les étudiants, enseignants et personnels des écoles sous la direction
#         students = Student.objects.filter(school__in=schools)
#         teachers = Teacher.objects.filter(school__in=schools)
#         staff = Staff.objects.filter(school__in=schools)
#
#         context = {
#             'schools': schools,
#             'students': students,
#             'teachers': teachers,
#             'staff': staff,
#         }
#
#         return render(request, 'service/admin/dashboard.html', context)
#
#     except Employee.DoesNotExist:
#         raise PermissionDenied




