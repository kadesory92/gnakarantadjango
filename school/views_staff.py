from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators_middleware import required_role
from account.forms import UserForm
from service.models import Employee
from .forms import StaffForm
from .models import School, Staff


@login_required(login_url='login')
@required_role(['ADMIN_DPE', 'ADMIN_DCE', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER', 'SCHOOL'])
def manage_staff(request):

    query = request.POST.get('q')
    if request.user.role in ['ADMIN_DPE', 'ADMIN_DCE']:
        employee = get_object_or_404(Employee, user=request.user)
        service = employee.service
        school = get_object_or_404(School, direction=service)
    elif request.user in ['SCHOOL_ADMIN', 'SCHOOL_MANAGER']:
        staff = get_object_or_404(Staff, user=request.user)
        school = staff.school
    else:
        school = get_object_or_404(School, user=request.user)
    staffs = Staff.objects.filter(school=school).order_by('lastname')
    if query:
        staffs = staffs.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(position__icontains=query)
        )
    # Pagination
    paginator = Paginator(staffs, 10)  # 10 staffs by page
    page = request.GET.get('page')
    try:
        staffs = paginator.page(page)
    except PageNotAnInteger:
        # Si la page n'est pas un entier, afficher la première page
        staffs = paginator.page(1)
    except EmptyPage:
        # Si la page est vide, afficher la dernière page
        staffs = paginator.page(paginator.num_pages)
    context = {
        'staffs': staffs,
        'query': query
    }

    return render(request, 'core/school/staff/manage_staff.html', context)


@login_required(login_url='login')
@required_role(['ADMIN_DPE', 'ADMIN_DCE', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER', 'SCHOOL'])
def create_staff(request):
    if request.user.role in ['ADMIN_DPE', 'ADMIN_DCE']:
        employee = get_object_or_404(Employee, user=request.role)
        service = employee.service
        school = get_object_or_404(School, direction=service)
    elif request.user.role in ['SCHOOL_ADMIN', 'SCHOOL_MANAGER', '']:
        staff = get_object_or_404(Staff, user=request.user)
        school = staff.school
    else:
        school = get_object_or_404(School, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST, request.FILES)
        user_form.fields['role'].choices = [
            ('SCHOOL_ADMIN', 'Administrateur d\'école'),
            ('SCHOOL_MANAGER', 'Gestionnaire d\'école'),
            ('SCHOOL_STAFF', 'Personnels d\'école')
        ]
        if user_form.is_valid() and staff_form.is_valid():

            user = user_form.save(commit=False)
            user.save()

            staff = staff_form.save(commit=False)
            staff.user = user
            staff.school = school
            staff.save()
            return redirect('manage_staff')

    else:
        user_form = UserForm()
        staff_form = StaffForm()

        user_form.fields['role'].choices = [
            ('SCHOOL_ADMIN', 'Administrateur d\'école'),
            ('SCHOOL_MANAGER', 'Gestionnaire d\'école'),
            ('SCHOOL_STAFF', 'Personnels d\'école')
        ]
    return render(request, 'core/school/staff/create_staff.html', {'user_form': user_form, 'staff_form': staff_form})


def detail_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    context = {
        'staff': staff,
    }
    return render(request, 'core/school/staff/detail_staff.html', context)


def edit_staff(request):
    return render(request, 'core/school/staff/edit_staff.html')


def delete_staff(request,staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        staff.delete()
        return redirect('manage_staff')

    context = {
        'staff': staff
    }
    return render(request, 'core/school/staff/staff_delete_confirm.html', context)


