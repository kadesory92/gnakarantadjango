from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.shortcuts import render, redirect

from core.models import Student, Teacher
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
    schools = School.objects.all()
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    total_schools = schools.count()
    total_students = students.count()
    total_teachers = teachers.count()

    schools = schools.annotate(
        student_count=Count('student'),
        teacher_count=Count('schoolteacher')
    )

    # Filtering
    query = request.GET.get('q')
    direction_query = request.GET.get('direction')
    ire_query = request.GET.get('ire')
    type_query = request.GET.get('type')

    if query:
        schools = schools.filter(name__icontains=query)
    if direction_query:
        schools = schools.filter(direction__name__icontains=direction_query)
    if ire_query:
        schools = schools.filter(ire__name__icontains=ire_query)
    if type_query:
        schools = schools.filter(type__icontains=type_query)

    # Add ordering to ensure consistent pagination
    schools = schools.order_by('name')  # Remplacez 'name' par le champ approprié

    # Pagination
    paginator = Paginator(schools, 10)  # Show 10 services per page
    page = request.GET.get('page')
    try:
        schools = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, display the first page
        schools = paginator.page(1)
    except EmptyPage:
        # If the page is out of bounds (for example, 9999), display the last results page
        schools = paginator.page(paginator.num_pages)

    context = {
        'schools': schools,
        'query': query,
        'direction_query': direction_query,
        'ire_query': ire_query,
        'type_query': type_query,
        'total_schools': total_schools,
        'total_students': total_students,
        'total_teachers': total_teachers
    }
    return render(request, 'admin/admin_dashboard.html', context)


@login_required
def dashboard_redirect(request):
    user = request.user
    if user.role == 'ADMIN':
        return redirect('admin-dashboard')
    if user.role in ['ADMIN', 'SCHOOL', 'SCHOOL_ADMIN', 'SCHOOL_MANAGER', 'SCHOOL_STAFF']:
        return redirect('school_dashboard')
    if user.role in ['ADMIN', 'SERVICE_ADMIN', 'SERVICE_MANAGER', 'ADMIN_IRE', 'ADMIN_DPE', 'ADMIN_DCE']:
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


