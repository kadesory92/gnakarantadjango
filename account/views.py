from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from school.models import School
from service.models import Service
from .forms import EmployeeForm, UserForm, FounderForm, LoginForm
from .models import User


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page.
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logOut(request):
    logout(request)
    # Redirect to a success page.
    return redirect('home')  # Replace 'home' with the name of your home page URL


@login_required(login_url='login')
def admin_dashboard(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', '')
    filter_level = request.GET.get('level', '')
    filter_direction = request.GET.get('direction', '')
    filter_ire = request.GET.get('ire', '')

    schools = School.objects.all()

    if query:
        schools = schools.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )

    if filter_type:
        schools = schools.filter(type=filter_type)

    if filter_level:
        schools = schools.filter(level=filter_level)

    if filter_direction:
        schools = schools.filter(direction__id=filter_direction)

    if filter_ire:
        schools = schools.filter(ire__id=filter_ire)

    paginator = Paginator(schools, 10)  # Show 10 schools per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    directions = Service.objects.all()  # Assuming Service model represents directions
    ires = Service.objects.all()  # Assuming Service model represents IREs
    return render(request, 'admin/admin_dashboard.html', {
        'page_obj': page_obj,
        'query': query,
        'filter_type': filter_type,
        'filter_level': filter_level,
        'filter_direction': filter_direction,
        'filter_ire': filter_ire,
        'directions': directions,
        'ires': ires,
    })


@login_required
def dashboard(request):
    user = request.user
    if user.role == 'ADMIN':
        return redirect('admin-dashboard')
    if user.role in ['SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER', 'SCHOOL_STAFF']:
        return redirect('school_dashboard')
    if user.role in ['SERVICE_ADMIN', 'SERVICE_MANAGER', 'ADMIN_IRE', 'ADMIN_DPE', 'ADMIN_DCE']:
        return redirect('service_dashboard')
    else:
        return redirect('error')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        # Set the role choices to only ADMIN
        user_form.fields['role'].choices = [
            ('FOUNDER', 'Fondateur'),
            ('ADMIN', 'Administrateur')
        ]

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            # Redirect based on role
            if user.role == 'ADMIN':
                # Check if a user with the role ADMIN already exists
                if User.objects.filter(role='ADMIN').exists():
                    messages.error(request, 'An admin user already exists.')
                    return redirect('register')
                else:
                    user.save()
                    login(request, user)
                    messages.success(request, 'Admin user registered successfully!')
                    return redirect('home')  # Change to your actual admin dashboard URL
            elif user.role == 'FOUNDER':
                user.save()
                login(request, user)
                messages.success(request, 'Founder user registered successfully!')
                return redirect('register_founder')  # Change to your actual founder dashboard URL
        else:
            messages.error(request, 'There was an error in the form. Please correct the errors below.')
    else:
        user_form = UserForm()

        # Set the role choices to only ADMIN
        user_form.fields['role'].choices = [
            ('FOUNDER', 'Fondateur'),
            ('ADMIN', 'Administrateur')
        ]

    return render(request, 'auth/register.html', {'user_form': user_form})


@login_required()
def register_founder(request):
    # user = request.user
    if request.method == 'POST':

        founder_form = FounderForm(request.POST, request.FILES)

        if founder_form.is_valid():
            founder = founder_form.save(commit=False)
            founder.user = request.user
            founder.save()
            return redirect('home')  # Redirect to some view after registration
    else:

        founder_form = FounderForm()

    return render(request, 'auth/register_founder.html', {'founder_form': founder_form})


def register_employee(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        employee_form = EmployeeForm(request.POST, request.FILES)

        # Filter roles for employee registration
        user_form.fields['role'].choices = [
            ('SERVICE_STAFF', 'Service Staff'),
            ('ADMIN_IRE', 'Admin IRE'),
            ('ADMIN_DPE', 'Admin DPE'),
            ('ADMIN_DCE', 'Admin DCE'),
            ('STAFF_IRE', 'Personnel de IRE'),
            ('STAFF_DCE', 'Personnel de DCE'),
            ('STAFF_DPE', 'Personnel de DPE')
        ]

        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            messages.success(request, 'Employee registered successfully!')
            return redirect('admin-dashboard')
        else:
            messages.error(request, 'There was an error in the form. Please correct the errors below.')
    else:
        user_form = UserForm()
        employee_form = EmployeeForm()

        # Filter roles for employee registration
        user_form.fields['role'].choices = [
            ('SERVICE_STAFF', 'Service Staff'),
            ('ADMIN_IRE', 'Admin IRE'),
            ('ADMIN_DPE', 'Admin DPE'),
            ('ADMIN_DCE', 'Admin DCE'),
            ('STAFF_IRE', 'Personnel de IRE'),
            ('STAFF_DCE', 'Personnel de DCE'),
            ('STAFF_DPE', 'Personnel de DPE')
        ]

    return render(request, 'auth/register_employee.html', {
        'user_form': user_form,
        'employee_form': employee_form
    })


def error(request):
    return render(request, 'error.html')


