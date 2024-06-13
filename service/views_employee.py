from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from core.models import Teacher, Student
from school.models import Staff, School
from service.models import Employee, Service


@login_required
def list_employee_by_service(request):
    user = request.user

    if user.role in [
        'SERVICE_ADMIN', 'SERVICE_MANAGER', 'SERVICE_STAFF',
        'ADMIN_IRE', 'ADMIN_DPE', 'ADMIN_DCE', 'STAFF_IRE',
        'STAFF_DCE', 'STAFF_DPE'
    ]:
        employee = get_object_or_404(Employee, user=user)
        service = employee.service

    elif user.role == ['ADMIN_SCHOOL', 'SCHOOL_MANAGER', 'SCHOOL_STAFF']:

        staff = get_object_or_404(Staff, user=user)

        school = staff.school

        service = school.direction

    elif user.role == 'SCHOOL':

        school = get_object_or_404(School, user=user)

        service = school.direction

    elif user.role == 'TEACHER':
        teacher = get_object_or_404(Teacher, user=user)
        service = teacher.direction
    else:
        student = get_object_or_404(Student, user=user)
        school = student.school
        service = school.direction

    # Récupérer tous les employés du service
    employees = Employee.objects.filter(service=service).order_by('lastname')

    # Gestion de la recherche
    query = request.GET.get('q')
    if query:
        employees = employees.filter(
            Q(lastname__icontains=query) |
            Q(firstname__icontains=query) |
            Q(user__email__icontains=query) |
            Q(position__icontains=query) |
            Q(phone__icontains=query)
        )

    # Gestion de la pagination
    paginator = Paginator(employees, 10)  # 10 employés par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'service/admin/employee/list_employee_by_service.html', {
        'employees': page_obj,
        'query': query,
    })


def employee(request, id):
    employee = get_object_or_404(Employee, pk=id)
    return render(request, 'service/employee/employee.html', {'employee': employee})



